from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int
    db_table: str
    db_theme: str


def create_paginator(db_table: str, db_theme: str):
    print(db_table, db_theme)

    def paginator(page: int = 0):
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page, db_table=db_table,
                                                                     db_theme=db_theme).pack()),
            InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, db_table=db_table,
                                                                     db_theme=db_theme).pack()),
            InlineKeyboardButton(text="🔙", callback_data=f'topic:{db_table}'),
            width=2
        )
        return builder.as_markup()

    return paginator


def greeting():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Теми', callback_data='topics'),
        InlineKeyboardButton(text='Розробники', callback_data='devs'),
        InlineKeyboardButton(text='Про бота', callback_data='bot_info'),
        InlineKeyboardButton(text='Перекладач', callback_data='translate'),
        width=2
    )
    return builder.as_markup()
