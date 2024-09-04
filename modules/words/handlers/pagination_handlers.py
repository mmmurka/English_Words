from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from layers.functions.cb_decoder import decode_table
from layers.functions.cb_encoder import encode_table
from modules.words.data.data_retriever import get_group_subjects
from modules.words.keyboards.paginators import Pagination, create_group_subject_paginator

router = Router()

@router.callback_query(F.data.startswith("pag:"))
async def handle_pagination(call: CallbackQuery):
    # Разбиваем данные на части

    data_parts = call.data.split(':')
    action = data_parts[1]   # "next" или "prev"
    page_num = int(data_parts[2])
    type_of_pagination = data_parts[3]
    table_name = data_parts[4]
    decoded_table_name = decode_table(table_name)
    if type_of_pagination == 'gs':
        groups_of_subject = await get_group_subjects(decoded_table_name)
        groups_of_subject = [groups_of_subject[i:i + 10] for i in range(0, len(groups_of_subject), 10)]
        # Обрабатываем "prev" и "next"
        if action == "prev":
            page_num = max(page_num - 1, 0)
        elif action == "next":
            page_num = min(page_num + 1, len(groups_of_subject) - 1)

        paginator = await create_group_subject_paginator(table_name)


        # Безопасное обновление сообщения
        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                f"Оберіть тему:",
                reply_markup=paginator(page_num)
            )

