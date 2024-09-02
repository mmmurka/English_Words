from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
# from layers.functions.cb_encoder import encode_table, encode_group_subject
from modules.words.data.data_retriever import get_group_subjects


class Pagination(CallbackData, prefix="paginator"):
    action: str
    page: int
    table_name: str
    group_subject: str
    subject: str

class GroupSubjectPagination(CallbackData, prefix="group_subject"):
    action: str
    page: int
    db_table: str


class SubjectPagination(CallbackData, prefix="subject"):
    action: str
    page: int
    db_table: str
    db_group_subject: str

#function that handles pagination and change pages

async def handle_pagination_action(action: str, page: int, total_pages: int) -> int:
    if action == "prev":
        return max(0, page - 1)
    elif action == "next":
        return min(total_pages - 1, page + 1)
    return page


async def create_subject_paginator(table_name: str):
    groups_of_subject = await get_group_subjects(table_name)
    groups_of_subject = list(map(lambda x: x.capitalize(), groups_of_subject))
    groups_of_subject = [groups_of_subject[i:i + 10] for i in range(0, len(groups_of_subject), 10)]
    def group_subject_paginator(page: int = 0):
        builder = InlineKeyboardBuilder()
        [builder.button(text=group_subject, callback_data='None') for group_subject in groups_of_subject[page]]
        builder.adjust(1)
        builder.row(
            InlineKeyboardButton(text="⬅️", callback_data=GroupSubjectPagination(action="prev", page=page,
                                                                                 db_table=table_name).pack()),
            InlineKeyboardButton(text="➡️", callback_data=GroupSubjectPagination(action="next", page=page,
                                                                                 db_table=table_name).pack()),
            InlineKeyboardButton(text="Назад", callback_data='word_tables'),
            width=2
        )
        return builder.as_markup()

    return group_subject_paginator