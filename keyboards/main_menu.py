from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from utils.crud import ScheduleCRUD


def get_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔍 Расписание занятий')
    builder.button(text='✏️ Записаться на пробное занятие')
    builder.button(text='🎯 Акции и скидки')
    builder.button(text='💬 Связаться с нами')
    builder.button(text='📍 Где мы находимся?')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

def user_back_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='◀️ Главное меню')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

def choose_direction_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🎭 Актёрское мастерство', callback_data='actor')
    builder.button(text='🎸 Игра на гитаре', callback_data='guitar')
    builder.button(text='🥁 Игра на барабанах', callback_data='drums')
    builder.button(text='💼 Программирование', callback_data='programming')
    builder.button(text='◀️ Главное меню', callback_data='back')

    builder.adjust(2, 2)

    return builder.as_markup()

def app_choose_section() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🎭 Актёрское мастерство')
    builder.button(text='🎸 Игра на гитаре')
    builder.button(text='🥁 Игра на барабанах')
    builder.button(text='💼 Программирование')
    builder.button(text='◀️ Главное меню')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )


def app_choose_location() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='ст. Новотитаровская, ул. Широкая 52')
    builder.button(text='мкр. Молодёжный, ул. 2-я Целеноградская 11')
    builder.button(text='Энка, ул. Покрышкина 2/1')
    builder.button(text='◀️ Главное меню')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )


async def schedule_choose_time(section: str, location: str, message: types.Message) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    found_schedules = False
    for schedule in await ScheduleCRUD.get_all_schedules():
        if schedule.section == section and schedule.location == location:

            builder.button(text=f'{schedule.time}')
            found_schedules = True

    builder.button(text='◀️ Главное меню')
    if not found_schedules:
        await message.answer('Нет подходящих расписаний. Введите желаемое время.')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )


