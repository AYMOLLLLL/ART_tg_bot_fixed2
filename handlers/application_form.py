from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_menu import app_choose_section, app_choose_location, get_main_menu, user_back_kb, schedule_choose_time

from config import ADMIN_IDS

router = Router()

class ApplicationForm(StatesGroup):
    name = State()
    age = State()
    section = State()
    location = State()
    time = State()
    phone = State()

@router.message(F.text == '✏️ Записаться на пробное занятие')
async def start_application(message: types.Message, state: FSMContext):
    await message.answer('Введите имя ученика', reply_markup=user_back_kb())
    await state.set_state(ApplicationForm.name)

@router.message(ApplicationForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите возраст ученика', reply_markup=user_back_kb())
    await state.set_state(ApplicationForm.age)

@router.message(ApplicationForm.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Выберите название направления:', reply_markup=app_choose_section())
    await state.set_state(ApplicationForm.section)

@router.message(ApplicationForm.section)
async def process_section(message: types.Message, state: FSMContext):
    await state.update_data(section=message.text)
    await message.answer('Выберите удобное вам место:', reply_markup=app_choose_location())
    await state.set_state(ApplicationForm.location)

@router.message(ApplicationForm.location)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    filtration = await state.get_data()
    keyboard = await schedule_choose_time(filtration['section'], filtration['location'], message)
    await message.answer('Введите удобное вам время', reply_markup= keyboard)
    await state.set_state(ApplicationForm.time)

@router.message(ApplicationForm.time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer('Введите ваш номер телефона', reply_markup=user_back_kb())
    await state.set_state(ApplicationForm.phone)

@router.message(ApplicationForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    user = message.from_user
    username = f"@{user.username}" if user.username else "Не указан"
    await message.answer(f"Заявка заполнена!\n"
                         f"Имя: {data['name']}\n"
                         f"Возраст: {data['age']}\n"
                         f"Направление: {data['section']}\n"
                         f"Филиал: {data['location']}\n"
                         f"Желаемое время: {data['time']}\n"
                         f"Ваш номер телефона: {data['phone']}", reply_markup=get_main_menu())

    for admin_id in ADMIN_IDS:
        await message.bot.send_message(admin_id, f"Новая заявка:\n"
                                                      f"Имя: {data['name']}\n"
                                                      f"Возраст: {data['age']}\n"
                                                      f"Место: {data['location']}\n"
                                                      f"Время: {data['time']}\n"
                                                      f"Телефон: {data['phone']}\n"
                                                      f"Телеграм: {username}")



    await state.clear()