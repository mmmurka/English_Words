from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from layers.functions.cb_decoder import decode_table, decode_group_subject
from layers.functions.cb_encoder import encode_group_subject, encode_subject
from layers.functions.common import normalize_list
from modules.words.data.repository import WordRepository
from postgres.controller.database import DBManager

repo = WordRepository(DBManager().getSession)

class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int
    type_of_pagination: str
    table_name: str
    group_subject: str or list[str] = None
    subject: str = None
    gs_page: int = 0
    s_page: int = 0


async def create_group_subject_paginator(table_name: str):
    encoded_table_name: str = table_name
    decoded_table_name: str = decode_table(table_name)
    groups_of_subject: list = await repo.get_distinct_group_subjects(decoded_table_name)
    groups_of_subject: list = list(map(lambda x: x.capitalize(), groups_of_subject))
    count_groups: int = len(groups_of_subject)
    if count_groups > 10:
        groups_of_subject = normalize_list(groups_of_subject)

    def group_subject_paginator_cb(page: int = 0):
        builder = InlineKeyboardBuilder()
        group_subject_page = page
        if count_groups > 10:
            [builder.button(text=group_subject,
                            callback_data=f'subjects:{encoded_table_name}:{encode_group_subject(group_subject)}:{group_subject_page}')
             for group_subject in groups_of_subject[page]]
            builder.adjust(1)
            builder.row(
                InlineKeyboardButton(text="⬅️",
                                     callback_data=Pagination(action="prev", page=page, type_of_pagination='gs',
                                                              table_name=encoded_table_name,
                                                              group_subject_page=group_subject_page).pack()),
                InlineKeyboardButton(text=f'{page + 1}/{len(groups_of_subject)}', callback_data='None'),
                InlineKeyboardButton(text="➡️",
                                     callback_data=Pagination(action="next", page=page, type_of_pagination='gs',
                                                              table_name=encoded_table_name,
                                                              group_subject_page=group_subject_page).pack()),
                InlineKeyboardButton(text="Назад", callback_data='word_tables'),
                width=3)

        else:
            [builder.button(text=group_subject,
                            callback_data=f'subjects:{encoded_table_name}:{encode_group_subject(group_subject)}:{group_subject_page}')
             for group_subject in groups_of_subject]
            builder.button(text="Назад", callback_data='word_tables')
            builder.adjust(1)

        return builder.as_markup()

    return group_subject_paginator_cb


async def create_subject_paginator(table_name: str, group_subject: str, gs_page: int):
    encoded_table_name: str = table_name
    decoded_table_name: str = decode_table(table_name)
    encoded_group_subject: str = group_subject
    decoded_group_subject: str = decode_group_subject(group_subject)
    subjects: list = await repo.get_distinct_subjects(decoded_table_name, decoded_group_subject)
    subjects: list = list(map(lambda x: x.capitalize(), subjects))
    count_subjects: int = len(subjects)
    if count_subjects > 10:
        subjects = normalize_list(subjects)

    def subject_paginator_cb(page: int = 0):
        builder = InlineKeyboardBuilder()
        subject_page = page
        if count_subjects > 10:
            [builder.button(text=subject,
                            callback_data=f'words:{encoded_table_name}:{encoded_group_subject}:{encode_subject(subject)}:{gs_page}:{subject_page}')
             for subject in subjects[page]]
            builder.adjust(1)
            builder.row(
                InlineKeyboardButton(text="⬅️",
                                     callback_data=Pagination(action="prev", page=page, type_of_pagination='s',
                                                              table_name=encoded_table_name,
                                                              group_subject=encoded_group_subject, gs_page=gs_page,
                                                              s_page=subject_page).pack()),
                InlineKeyboardButton(text=f'{page + 1}/{len(subjects)}', callback_data='None'),
                InlineKeyboardButton(text="➡️",
                                     callback_data=Pagination(action="next", page=page, type_of_pagination='s',
                                                              table_name=encoded_table_name,
                                                              group_subject=encoded_group_subject, gs_page=gs_page,
                                                              s_page=subject_page).pack()),
                InlineKeyboardButton(text="Назад", callback_data=f'group_subject:{encoded_table_name}:{gs_page}'),
                width=3)

        else:
            [builder.button(text=subject,
                            callback_data=f'words:{encoded_table_name}:{encoded_group_subject}:{encode_subject(subject)}:{gs_page}:{subject_page}')
             for subject in subjects]
            builder.button(text="Назад", callback_data=f'group_subject:{encoded_table_name}:{gs_page}')
            builder.adjust(1)

        return builder.as_markup()

    return subject_paginator_cb


async def create_word_paginator(table_name: str, group_subject: str, subject: str, state: FSMContext, gs_page: int,
                                s_page: int):
    encoded_table_name: str = table_name
    encoded_group_subject: str = group_subject
    encoded_subject: str = subject
    data: dict = await state.get_data()
    words: str = data['words']

    def word_paginator_cb(page: int = 0):
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="🇺🇦", callback_data=Pagination(action="trans", page=page, type_of_pagination='w',
                                                                     table_name=encoded_table_name,
                                                                     group_subject=encoded_group_subject,
                                                                     subject=encoded_subject).pack()),
            InlineKeyboardButton(text="➕", callback_data='None'),
            InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page, type_of_pagination='w',
                                                                     table_name=encoded_table_name,
                                                                     group_subject=encoded_group_subject,
                                                                     subject=encoded_subject, gs_page=gs_page,
                                                                     s_page=s_page).pack()),
            InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, type_of_pagination='w',
                                                                     table_name=encoded_table_name,
                                                                     group_subject=encoded_group_subject,
                                                                     subject=encoded_subject, gs_page=gs_page,
                                                                     s_page=s_page).pack()),
            InlineKeyboardButton(text="Назад",
                                 callback_data=f'subjects:{encoded_table_name}:{encoded_group_subject}:{gs_page}:{s_page}'),
            width=2)

        return builder.as_markup()

    return word_paginator_cb
