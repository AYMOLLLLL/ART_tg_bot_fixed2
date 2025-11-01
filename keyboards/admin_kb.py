from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from utils.crud import ScheduleCRUD

def admin_main_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='Редактировать направления')
    builder.button(text='Добавить направления')
    builder.button(text='Добавить/редактировать текст с акциями')
    builder.button(text='Удалить текст с акциями')
    builder.button(text='◀️ Главное меню')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

def admin_back_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='◀️ Назад')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

def admin_choose_section_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🎭 Актёрское мастерство')
    builder.button(text='🎸 Игра на гитаре')
    builder.button(text='🥁 Игра на барабанах')
    builder.button(text='💼 Программирование')
    builder.button(text='◀️ Назад')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

def admin_choose_location_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='ст. Новотитаровская, ул. Широкая 52')
    builder.button(text='мкр. Молодёжный, ул. 2-я Целеноградская 11')
    builder.button(text='Энка, ул. Покрышкина 2/1')
    builder.button(text='◀️ Назад')

    builder.adjust(2, 2)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )


async def schedule_filtration(section: str, location: str, message: types.Message):
    found_schedules = False
    for schedule in await ScheduleCRUD.get_all_schedules():
        if schedule.section == section and schedule.location == location:
            markup = admin_edit_btn(schedule)

            await message.answer(f'{schedule.section}: {schedule.time}, свободных мест: {schedule.free_place}', reply_markup=markup)
            found_schedules = True

    if not found_schedules:
        await message.answer('Нет подходящих расписаний.', reply_markup=admin_back_kb())
    else:
        await message.answer('Вот список всех расписаний🔼', reply_markup=admin_back_kb())


def admin_edit_btn(schedule) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Редактировать', callback_data=f'edit_{schedule.id}')
    builder.button(text='Удалить', callback_data=f'delete_{schedule.id}')

    return builder.as_markup()

def admin_edit_promotion() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Редактировать текст', callback_data='redit_promotion')
    builder.button(text='◀️ Назад', callback_data='admin_main')

    builder.adjust(2, 2)

    return builder.as_markup()

def admin_add_promotion() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Добавить текст', callback_data='add_promotion')
    builder.button(text='◀️ Назад', callback_data='admin_main')

    builder.adjust(2, 2)

    return builder.as_markup()

def admin_delete_promotion() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Удалить текст', callback_data='del_promotion')
    builder.button(text='◀️ Назад', callback_data='admin_main')

    builder.adjust(2, 2)

    return builder.as_markup()