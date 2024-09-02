from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from layers.functions.cb_encoder import encode_table, encode_group

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


