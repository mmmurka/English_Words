from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from layers.functions.cb_decoder import decode_table, decode_group_subject

from layers.functions.common import normalize_list
from modules.words.data.repository import WordRepository

from modules.words.keyboards.paginators import (
    create_group_subject_paginator,
    create_subject_paginator,
    create_word_paginator,
)
from layers.translate_api.translateAPI import trans_text
from postgres.controller.database import DBManager

repo = WordRepository(DBManager().getSession)
router = Router()


@router.callback_query(F.data.startswith("pag:"))
async def handle_pagination(call: CallbackQuery, state: FSMContext):

    data_parts: list = call.data.split(":")  # Breaking data into parts
    action: str = data_parts[1]  # "next" or "prev"
    page: int = int(data_parts[2])
    type_of_pagination = data_parts[3]
    table_name = data_parts[4]
    gs_page = int(data_parts[7])
    s_page = int(data_parts[8])
    decoded_table_name = decode_table(table_name)
    if type_of_pagination == "gs":
        groups_of_subject = await repo.get_distinct_group_subjects(decoded_table_name)
        groups_of_subject = normalize_list(groups_of_subject)
        # Обрабатываем "prev" и "next"
        if action == "prev":
            page = max(page - 1, 0)
        elif action == "next":
            page = min(page + 1, len(groups_of_subject) - 1)

        paginator = await create_group_subject_paginator(table_name)

        with suppress(TelegramBadRequest):
            await call.message.edit_text(f"Оберіть тему:", reply_markup=paginator(page))

    elif type_of_pagination == "s":  # subjects
        try:
            group_subject = data_parts[5]
            decoded_group_subject = decode_group_subject(group_subject)
        except IndexError:
            raise IndexError("Не передано назву теми")

        subjects: list = await repo.get_distinct_subjects(decoded_table_name, decoded_group_subject)
        subjects: list = normalize_list(subjects)
        # Обрабатываем "prev" и "next"
        if action == "prev":
            page = max(page - 1, 0)
        elif action == "next":
            page = min(page + 1, len(subjects) - 1)

        paginator = await create_subject_paginator(table_name, group_subject, gs_page)

        with suppress(TelegramBadRequest):
            await call.message.edit_text(f"Оберіть тему:", reply_markup=paginator(page))
    elif type_of_pagination == "w":  # words
        try:
            group_subject = data_parts[5]
            subject = data_parts[6]
        except IndexError:
            raise IndexError("Не передано назву теми")



        # words, definitions = await get_words(decoded_table_name, decoded_group_subject, decoded_subject)
        data: dict = await state.get_data()
        words: str = data["words"]
        definitions: str = data["definitions"]
        if action == "prev":
            page = max(page - 1, 0)
        elif action == "next":
            page = min(page + 1, len(words) - 1)

        paginator = await create_word_paginator(
            table_name, group_subject, subject, state, gs_page, s_page
        )

        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                f"{words[page]} - {definitions[page]}", reply_markup=paginator(page)
            )
        await call.answer()

        if action == "trans":
            result_translate = await trans_text(text=words[page] + " - " + definitions[page], src='en', dest='uk')
            with suppress(TelegramBadRequest):
                await call.message.edit_text(
                    f"{words[page]} - {definitions[page]}\n\n\n{result_translate}",
                    reply_markup=paginator(page)
                )
            await call.answer()
