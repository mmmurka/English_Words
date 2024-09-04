from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from layers.functions.cb_decoder import decode_table
from layers.functions.cb_encoder import encode_table, encode_group_subject
# from layers.functions.cb_encoder import encode_table, encode_group_subject
from modules.words.data.data_retriever import get_group_subjects


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int
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
        groups_of_subject = [groups_of_subject[i:i + 10] for i in range(0, len(groups_of_subject), 10)]
    def group_subject_paginator(page: int = 0):
        builder = InlineKeyboardBuilder()
        if count_groups > 10:
            [builder.button(text=group_subject, callback_data=f'subjects:{encoded_table_name}:{encode_group_subject(group_subject)}') for group_subject in groups_of_subject[page]]
            builder.adjust(1)
            builder.row(
                InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page, table_name=encoded_table_name).pack()),
                InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page, table_name=encoded_table_name).pack()),
                InlineKeyboardButton(text="Назад", callback_data='word_tables'),
                width=2)

        else:
            [builder.button(text=group_subject, callback_data=f'subjects:{encoded_table_name}:{encode_group_subject(group_subject)}') for group_subject in groups_of_subject]
            builder.button(text="Назад", callback_data='word_tables')
            builder.adjust(1)

        return builder.as_markup()

    return group_subject_paginator