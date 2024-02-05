from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from Telegram.callbacks.topics import group_from_theme


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int
    db_table: str
    db_theme: str


async def create_paginator(db_table: str, db_theme: str):
    if db_table == 'most_common':
        group_subject = db_theme
    else:
        group_subject = await group_from_theme(db_table, db_theme)
        group_subject = ' '.join(group_subject)
        if len(group_subject) > 15:
            group_subject = group_subject[:15]

    def paginator(page: int = 0):

        if db_table != 'most_common':
            builder = InlineKeyboardBuilder()
            builder.row(
                InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page, db_table=db_table,
                                                                         db_theme=db_theme).pack()),
                InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, db_table=db_table,
                                                                         db_theme=db_theme).pack()),

                InlineKeyboardButton(text="Назад", callback_data=f'theme:{db_table}:{group_subject}'),

                InlineKeyboardButton(text='🇺🇦', callback_data=Pagination(action="trans", page=page, db_table=db_table,
                                                                         db_theme=db_theme).pack()),
                width=2
            )
        else:
            builder = InlineKeyboardBuilder()
            builder.row(
                InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page, db_table=db_table,
                                                                         db_theme=db_theme).pack()),
                InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, db_table=db_table,
                                                                         db_theme=db_theme).pack()),
                InlineKeyboardButton(text="Назад", callback_data=f'topic:{db_table}:{group_subject}'),

                InlineKeyboardButton(text='🇺🇦',
                                     callback_data=Pagination(action="trans", page=page, db_table=db_table,
                                                              db_theme=db_theme).pack()),
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
