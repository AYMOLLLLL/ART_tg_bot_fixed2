from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from keyboards.admin_kb import admin_main_kb, admin_choose_section_kb, admin_choose_location_kb, schedule_filtration ,admin_edit_btn, admin_back_kb, admin_edit_promotion, admin_add_promotion, admin_delete_promotion

from utils.crud import ScheduleCRUD, PromotionCRUD

from config import ADMIN_IDS

router = Router()

router.message.filter(F.from_user.id.in_(ADMIN_IDS))

VALID_SECTIONS = ['🎭 Актёрское мастерство', '🎸 Игра на гитаре', '🥁 Игра на барабанах', '💼 Программирование']
VALID_LOCATIONS = ['ст. Новотитаровская, ул. Широкая 52', 'мкр. Молодёжный, ул. 2-я Целеноградская 11', 'Энка, ул. Покрышкина 2/1']




@router.message(F.text == '◀️ Назад')
@router.message(Command("admin"))
async def admin_menu(message: types.Message, state: FSMContext):
    await message.answer('Вы перешли в админ-меню. Что будете делать?', reply_markup=admin_main_kb())
    await state.clear()

@router.callback_query(F.data == 'admin_main')
async def admin_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы перешли в админ-меню. Что будете делать?', reply_markup=admin_main_kb())
    await state.clear()
    await callback.answer()



class Edit(StatesGroup):
    section = State()
    location = State()


@router.message(F.text == 'Редактировать направления')
async def admin_edit_time_section(message: types.Message, state: FSMContext):
    await message.answer('Выберите направление:', reply_markup=admin_choose_section_kb())
    await state.set_state(Edit.section)


@router.message(Edit.section)
async def verification_section(message: types.Message, state: FSMContext):
    if message.text not in VALID_SECTIONS:
        await message.answer('Не правильный ввод. Выберите из предложенных вариантов.')
        return

    await state.update_data(section = message.text)
    await message.answer('Теперь выберите место:', reply_markup=admin_choose_location_kb())
    await state.set_state(Edit.location)

@router.message(Edit.location)
async def verification_location(message: types.Message, state: FSMContext):
    if message.text not in VALID_LOCATIONS:
        await message.answer('Не правильный ввод. Выберите из предложенных вариантов.')
        return

    await state.update_data(location = message.text)
    data = await state.get_data()
    await schedule_filtration(data['section'], data['location'], message)
    await state.clear()



class Add(StatesGroup):
    section = State()
    location = State()
    time = State()
    free_place = State()

@router.message(F.text == 'Добавить направления')
async def admin_add(message: types.Message, state: FSMContext):
    await message.answer('Выберите направление:', reply_markup=admin_choose_section_kb())
    await state.set_state(Add.section)

@router.message(Add.section)
async def verification_section(message: types.Message, state: FSMContext):
    if message.text not in VALID_SECTIONS:
        await message.answer('Не правильный ввод. Выберите из предложенных вариантов.')
        return

    await state.update_data(section = message.text)
    await message.answer('Теперь выберите место:', reply_markup=admin_choose_location_kb())
    await state.set_state(Add.location)

@router.message(Add.location)
async def verification_location(message: types.Message, state: FSMContext):
    if message.text not in VALID_LOCATIONS:
        await message.answer('Не правильный ввод. Выберите из предложенных вариантов.')
        return

    await state.update_data(location = message.text)
    await message.answer('Введите время(пример: Среда/пятница: 17:30)', reply_markup=admin_back_kb())
    await state.set_state(Add.time)

@router.message(Add.time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(time = message.text)
    await message.answer('Введите кол-во свободных мест(пример: 3)')
    await state.set_state(Add.free_place)

@router.message(Add.free_place)
async def process_free_place(message: types.Message, state: FSMContext):
    try:
        await state.update_data(free_place = message.text)
        data = await state.get_data()

        await ScheduleCRUD.create_schedule(data)

        await state.clear()

        await message.answer(
            f"✅ Направление успешно добавлено!\n"
            f"📍 Направление: {data['section']}\n"
            f"🏢 Место: {data['location']}\n"
            f"⏰ Время: {data['time']}\n"
            f"🎫 Свободных мест: {data['free_place']}",
            reply_markup=admin_main_kb()  # вернуться в главное меню
        )
    except Exception as e:
        await message.answer(f'Произошла ошибка при добавлении. Попробуйте ещё раз. ({e})')

class NewEdit(StatesGroup):
    section = State()
    location = State()
    time = State()
    free_place = State()

@router.callback_query(F.data.startswith('edit_'))
async def start_edit(callback: types.CallbackQuery, state: FSMContext):
    edit_id = int(callback.data.split('_')[-1])
    await state.update_data(schedule_id = edit_id)
    await callback.message.answer('Выберите новое название секции(или оставьте старое):', reply_markup=admin_choose_section_kb())
    await state.set_state(NewEdit.section)
    await callback.answer()

@router.message(NewEdit.section)
async def start_edit(message: types.Message, state: FSMContext):
    if message.text not in VALID_SECTIONS:
        await message.answer('Не правильный ввод. Выберите из предложенных вариантов.')
        return

    await state.update_data(section = message.text)
    await message.answer('Теперь выберите новое место(или оставьте старое):', reply_markup=admin_choose_location_kb())
    await state.set_state(NewEdit.location)

@router.message(NewEdit.location)
async def verification_location(message: types.Message, state: FSMContext):
    if message.text not in VALID_LOCATIONS:
        await message.answer('Не правильный ввод. Выберите из предложенных вариантов.')
        return

    await state.update_data(location = message.text)
    await message.answer('Введите время новое время(или оставьте старое), пример: Среда/пятница: 17:30', reply_markup=admin_back_kb())
    await state.set_state(NewEdit.time)

@router.message(NewEdit.time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(time = message.text)
    await message.answer('Введите кол-во свободных мест(пример: 3)')
    await state.set_state(NewEdit.free_place)

@router.message(NewEdit.free_place)
async def process_free_place(message: types.Message, state: FSMContext):
    try:
        await state.update_data(free_place = message.text)
        data = await state.get_data()

        schedule_id = data.pop('schedule_id')
        await ScheduleCRUD.update_schedule(schedule_id, data)

        await state.clear()

        await message.answer(
            f"✅ Направление успешно обновлено!\n"
            f"📍 Направление: {data['section']}\n"
            f"🏢 Место: {data['location']}\n"
            f"⏰ Время: {data['time']}\n"
            f"🎫 Свободных мест: {data['free_place']}",
            reply_markup=admin_main_kb()  # вернуться в главное меню
        )
    except Exception as e:
        await message.answer(f'Произошла ошибка при добавлении. Попробуйте ещё раз. ({e})')


@router.callback_query(F.data.startswith('delete_'))
async def process_delete_time(callback: types.CallbackQuery):
    schedule_id = int(callback.data.split('_')[-1])

    deleted_schedule = await ScheduleCRUD.delete_schedule(schedule_id)

    if deleted_schedule:
        await callback.message.answer("✅ Расписание успешно удалено!")
    else:
        await callback.message.answer("❌ Расписание не найдено!")

    await callback.answer()



@router.message(F.text == 'Добавить/редактировать текст с акциями')
async def add_edit_promotion(message: types.Message, state: FSMContext):
    promotion = await PromotionCRUD.get_all_promotions()
    if promotion:
        for prom in promotion:
            await message.answer(f'У вас уже есть текст с акциями:\n\n{prom.text}\n\n Нажмите, чтобы продолжить:', reply_markup=admin_edit_promotion())
    else:
        await message.answer('У вас ещё нет текста с акциями. Нажмите, чтобы продолжить:', reply_markup=admin_add_promotion())


class PromotionState(StatesGroup):
    text = State()

@router.callback_query(F.data == 'add_promotion')
@router.callback_query(F.data == 'redit_promotion')
async def handle_promotion(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите новый текст промо-акции:')
    await state.set_state(PromotionState.text)
    await callback.answer()

@router.message(PromotionState.text)
async def process_promotion_text(message: types.Message, state: FSMContext):
    # Текст промо-акции будет меняться ТОЛЬКО когда в этом состоянии
    promotion_data = {'text': message.text}
    await PromotionCRUD.delete_all_promotions()
    await PromotionCRUD.create_promotion(promotion_data)
    await message.answer('✅ Текст промо-акции обновлен!', reply_markup=admin_main_kb())
    await state.clear()  # очищаем состояние

@router.message(F.text == 'Удалить текст с акциями')
async def edit_promotion(message: types.Message):
    await message.answer('Вы уверены, что хотите удалить текст с акциями?', reply_markup=admin_delete_promotion())

@router.callback_query(F.data == 'del_promotion')
async def edit_promotion(callback: types.CallbackQuery):
    await PromotionCRUD.delete_all_promotions()
    await callback.message.answer('Текст с акциями удалён!', reply_markup=admin_main_kb())

    await callback.answer()