from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from layers.functions.cb_decoder import decode_table, decode_group_subject, decode_subject
from layers.functions.cb_encoder import encode_group_subject, encode_subject
from layers.functions.common import normalize_list
from modules.words.data.data_retriever import get_group_subjects, get_subjects, get_words


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int
    type_of_pagination: str
    table_name: str
    group_subject: str or list[str] = None
    subject: str = None


async def create_group_subject_paginator(table_name: str):
    encoded_table_name = table_name
    decoded_table_name = decode_table(table_name)
    groups_of_subject = await get_group_subjects(decoded_table_name)
    groups_of_subject = list(map(lambda x: x.capitalize(), groups_of_subject))
    count_groups = len(groups_of_subject)
    if count_groups > 10:
        groups_of_subject = normalize_list(groups_of_subject)
    def group_subject_paginator(page: int = 0):
        builder = InlineKeyboardBuilder()
        if count_groups > 10:
            [builder.button(text=group_subject, callback_data=f'subjects:{encoded_table_name}:{encode_group_subject(group_subject)}') for group_subject in groups_of_subject[page]]
            builder.adjust(1)
            builder.row(
                InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page,type_of_pagination='gs', table_name=encoded_table_name).pack()),
                InlineKeyboardButton(text=f'{page + 1}/{len(groups_of_subject)}', callback_data='None'),
                InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, type_of_pagination='gs', table_name=encoded_table_name).pack()),
                InlineKeyboardButton(text="Назад", callback_data='word_tables'),
                width=3)

        else:
            [builder.button(text=group_subject, callback_data=f'subjects:{encoded_table_name}:{encode_group_subject(group_subject)}') for group_subject in groups_of_subject]
            builder.button(text="Назад", callback_data='word_tables')
            builder.adjust(1)

        return builder.as_markup()

    return group_subject_paginator

async def create_subject_paginator(table_name: str, group_subject: str):
    encoded_table_name = table_name
    decoded_table_name = decode_table(table_name)
    encoded_group_subject = group_subject
    decoded_group_subject = decode_group_subject(group_subject)
    subjects = await get_subjects(decoded_table_name, decoded_group_subject)
    subjects = list(map(lambda x: x.capitalize(), subjects))
    count_subjects = len(subjects)
    if count_subjects > 10:
        subjects = normalize_list(subjects)

    def subject_paginator(page: int = 0):
        builder = InlineKeyboardBuilder()
        if count_subjects > 10:
            [builder.button(text=subject, callback_data=f'words:{encoded_table_name}:{encoded_group_subject}:{encode_subject(subject)}') for subject in subjects[page]]
            builder.adjust(1)
            builder.row(
                InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page, type_of_pagination='s', table_name=encoded_table_name, group_subject=encoded_group_subject).pack()),
                        InlineKeyboardButton(text=f'{page + 1}/{len(subjects)}', callback_data='None'),
                InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, type_of_pagination='s', table_name=encoded_table_name, group_subject=encoded_group_subject).pack()),
                InlineKeyboardButton(text="Назад", callback_data=f'group_subject:{encoded_table_name}'),
                width=3)

        else:
            [builder.button(text=subject, callback_data=f'words:{encoded_table_name}:{encoded_group_subject}:{encode_subject(subject)}') for subject in subjects]
            builder.button(text="Назад", callback_data=f'group_subject:{encoded_table_name}')
            builder.adjust(1)

        return builder.as_markup()

    return subject_paginator

async def create_word_paginator(table_name: str, group_subject: str, subject: str, state: FSMContext):
    encoded_table_name = table_name
    decoded_table_name = decode_table(table_name)
    encoded_group_subject = group_subject
    decoded_group_subject = decode_group_subject(group_subject)
    encoded_subject = subject
    decoded_subject = decode_subject(subject)
    data = await state.get_data()
    words = data['words']
    def word_paginator(page: int = 0):
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page, type_of_pagination='w',
                                                                     table_name=encoded_table_name,
                                                                     group_subject=encoded_group_subject, subject=encoded_subject).pack()),
            InlineKeyboardButton(text=f'{page + 1}/{len(words)}', callback_data='None'),
            InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, type_of_pagination='w',
                                                                     table_name=encoded_table_name,
                                                                     group_subject=encoded_group_subject, subject=encoded_subject).pack()),
            InlineKeyboardButton(text="Назад", callback_data=f'subjects:{encoded_table_name}:{encoded_group_subject}'),
            width=3)

        return builder.as_markup()

    return word_paginator