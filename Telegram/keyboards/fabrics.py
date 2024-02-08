from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from Telegram.callbacks.topics import group_from_theme, theme_from_topic, topic_from_table


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int
    db_table: str
    db_theme: str


class ThemePagination(CallbackData, prefix="theme_pag"):
    action: str
    page: int
    db_table: str
    db_group_subject: str
    theme_or_topic: str


async def create_paginator(db_table: str, db_theme: str):
    group_subject = await group_from_theme(db_table, db_theme)
    group_subject = ' '.join(group_subject)
    group_subject = group_subject[:15]

    print(group_subject)

    def paginator(page: int = 0):
        if db_table == 'most_common' or db_table == 'most common':
            cb_data = f'topic:{db_table}:{group_subject}'
        else:
            cb_data = f'theme:{db_table}:{group_subject}'
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page, db_table=db_table,
                                                                     db_theme=db_theme).pack()),
            InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, db_table=db_table,
                                                                     db_theme=db_theme).pack()),
            InlineKeyboardButton(text="Назад", callback_data=cb_data),

            InlineKeyboardButton(text='🇺🇦',
                                 callback_data=Pagination(action="trans", page=page, db_table=db_table,
                                                          db_theme=db_theme).pack()),
            width=2
        )

        return builder.as_markup()

    return paginator


async def create_theme_paginator(db_table: str, db_group_subject: str, theme_or_topic: str):
    if theme_or_topic == 'theme':
        themes = await theme_from_topic(' '.join(db_table.split('_')), ' '.join(db_group_subject.split('_')))
        themes_list = [themes[i:i + 10] for i in range(0, len(themes), 10)]
        cb_back = f'topic:{' '.join(db_table.split())}:{' '.join(db_group_subject.split())}'
    elif theme_or_topic == 'topic':
        themes = await topic_from_table(' '.join(db_table.split('_')))
        themes_list = [themes[i:i + 10] for i in range(0, len(themes), 10)]
        cb_back = f'topics'

    def theme_paginator(page: int = 0):
        builder = InlineKeyboardBuilder()
        if theme_or_topic == 'theme':

            if db_table == 'most_common' or db_table == 'most common':
                [builder.button(text=theme,
                                callback_data=f'words:{'_'.join(db_table.split())}:{'_'.join(theme.split())}') for
                 theme in themes_list[page]]
            else:
                [builder.button(text=theme,
                                callback_data=f'words:{'_'.join(db_table.split())}:{'_'.join(theme[:20].split())}') for
                 theme in themes_list[page]]


        elif theme_or_topic == 'topic':
            if db_table == 'most_common' or db_table == 'most common':
                [builder.button(text=theme,
                                callback_data=f'theme:{'_'.join(db_table.split())}:{'_'.join(theme.split())}') for
                 theme in themes_list[page]]
            else:
                [builder.button(text=theme,
                                callback_data=f'theme:{'_'.join(db_table.split())}:{'_'.join(theme[:20].split())}') for
                 theme in themes_list[page]]

        builder.adjust(1)

        builder.row(
            InlineKeyboardButton(text="⬅️", callback_data=ThemePagination(action="prev", page=page, db_table=db_table,
                                                                          db_group_subject=db_group_subject,
                                                                          theme_or_topic=theme_or_topic).pack()),
            InlineKeyboardButton(text="➡️", callback_data=ThemePagination(action="next", page=page, db_table=db_table,
                                                                          db_group_subject=db_group_subject,
                                                                          theme_or_topic=theme_or_topic).pack()),
            InlineKeyboardButton(text="Назад", callback_data=cb_back),
            width=2)

        return builder.as_markup()

    return theme_paginator


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
