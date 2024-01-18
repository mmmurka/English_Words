from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def paginator(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page).pack()),
        width=2
    )
    return builder.as_markup()


def greeting():
    builder = InlineKeyboardBuilder()
    builder.row(
       InlineKeyboardButton(text='Теми', callback_data='topics'),
       InlineKeyboardButton(text='Розробники', callback_data='devs'),
       InlineKeyboardButton(text='Про бота', callback_data='bot_info'),
       InlineKeyboardButton(text='Підримка', callback_data='support'),
       width=2
    )
    return builder.as_markup()



