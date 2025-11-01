from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from keyboards.admin_kb import admin_choose_section_kb, admin_choose_location_kb
from keyboards.main_menu import get_main_menu, choose_direction_kb, app_choose_section, app_choose_location
from utils.crud import ScheduleCRUD, PromotionCRUD

router = Router()

VALID_SECTIONS = ['🎭 Актёрское мастерство', '🎸 Игра на гитаре', '🥁 Игра на барабанах', '💼 Программирование']
VALID_LOCATIONS = ['ст. Новотитаровская, ул. Широкая 52', 'мкр. Молодёжный, ул. 2-я Целеноградская 11', 'Энка, ул. Покрышкина 2/1']



async def schedule_filtration_user(section: str, location: str, message: types.Message):
    found_schedules = False
    text = ''
    for schedule in await ScheduleCRUD.get_all_schedules():
        if schedule.section == section and schedule.location == location:

            text += f'{schedule.section}: {schedule.time}, свободных мест: {schedule.free_place}\n\n'
            found_schedules = True

    if not found_schedules:
        await message.answer('Нет подходящих расписаний.', reply_markup=get_main_menu())
    else:
        await message.answer('Вот список всех расписаний:', reply_markup=get_main_menu())
        await message.answer(text=text)


@router.message(F.text == '◀️ Главное меню')
@router.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext):
    welcome_text = """
<b>❗ Добро пожаловать в волшебный мир «То самого ART пространства»!</b>

<i>Это место, где мечты обретают крылья, а юные дарования раскрывают свои таланты:</i>

🎭 Актёрское мастерство 🎸 Игра на гитаре 🥁 Искусство игры на барабанах 💼 Программирование

Каждый ребёнок получит заботливое внимание наших преподавателей и раскроет свой творческий потенциал!<b>Давайте создавать шедевры вместе!</b>
    """
    keyboard = get_main_menu()

    await message.answer(welcome_text, reply_markup=keyboard)
    await state.clear()

@router.callback_query(F.data == 'back')
async def start_message(callback: types.CallbackQuery, state: FSMContext):
    welcome_text = """
<b>❗ Добро пожаловать в волшебный мир «То самого ART пространства»!</b>

<i>Это место, где мечты обретают крылья, а юные дарования раскрывают свои таланты:</i>

🎭 Актёрское мастерство 🎸 Игра на гитаре 🥁 Искусство игры на барабанах 💼 Программирование

Каждый ребёнок получит заботливое внимание наших преподавателей и раскроет свой творческий потенциал!<b>Давайте создавать шедевры вместе!</b>
    """
    keyboard = get_main_menu()

    await callback.message.answer(welcome_text, reply_markup=keyboard)
    await state.clear()
    await callback.answer()



class CheckSchedule(StatesGroup):
    section = State()
    location = State()

@router.message(F.text == '🔍 Расписание занятий')
async def schedule(message: types.Message, state: FSMContext):
    await message.answer('Выберите направление:', reply_markup=app_choose_section())
    await state.set_state(CheckSchedule.section)


@router.message(CheckSchedule.section)
async def verification_section(message: types.Message, state: FSMContext):
    if message.text not in VALID_SECTIONS:
        await message.answer('Не правильный ввод. Выберите из предложенных вариантов.')
        return

    await state.update_data(section=message.text)
    await message.answer('Теперь выберите место:', reply_markup=app_choose_location())
    await state.set_state(CheckSchedule.location)


@router.message(CheckSchedule.location)
async def verification_location(message: types.Message, state: FSMContext):
    if message.text not in VALID_LOCATIONS:
        await message.answer('Не правильный ввод. Выберите из предложенных вариантов.')
        return

    await state.update_data(location=message.text)
    data = await state.get_data()
    await schedule_filtration_user(data['section'], data['location'], message)
    await state.clear()

@router.message(F.text == '🎯 Акции и скидки')
async def discounts(message: types.Message):
    promotion = await PromotionCRUD.get_all_promotions()
    if promotion:
        for prom in promotion:
            await message.answer(f'Наши акции:\n\n{prom.text}')
    else:
        await message.answer('Сейчас акций нет')


@router.message(F.text == '💬 Связаться с нами')
async def contacts(message: types.Message):
    text = """
Контакты:
    
Whatsapp: 89384816294
    
Telegram: @Erema240
    """

    await message.answer(text)

@router.message(F.text == '📍 Где мы находимся?')
async def location(message: types.Message):
    text = """
📍 ст. Новотитаровская, ул. Широкая 52

📍 мкр. Молодёжный, ул. 2-я Целеноградская 11

📍 Энка, ул. Покрышкина 2/1
    """

    await message.answer(text)