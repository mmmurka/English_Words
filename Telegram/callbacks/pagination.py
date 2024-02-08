from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from Telegram.keyboards import fabrics
from Telegram.data.subloader import get_json
from Telegram.callbacks.topics import words_from_theme, theme_from_topic, topic_from_table
from Telegram.keyboards.fabrics import create_paginator, create_theme_paginator
from Telegram.translate.translateAPI import trans_text


router = Router()


@router.callback_query(fabrics.Pagination.filter(F.action.in_(["prev", "next", "trans"])))
async def pagination_handler(call: CallbackQuery, callback_data: fabrics.Pagination):
    table = callback_data.db_table.split('_')
    theme = callback_data.db_theme.split('_')
    buttons = await words_from_theme(' '.join(table), ' '.join(theme))
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(buttons) - 1) else page_num

    # Создаем экземпляр функции paginator с конкретными значениями db_table и db_theme
    my_paginator = await create_paginator(db_table=' '.join(table), db_theme=' '.join(theme))

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"{buttons[page]}",
            reply_markup=my_paginator(page)
        )
    await call.answer()

    if callback_data.action == "trans":
        page = page_num
        result_translate = await trans_text(text=buttons[page], src='en', dest='uk')
        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                f"{buttons[page]}\n\n\n{result_translate}",
                reply_markup=my_paginator(page)
            )
        await call.answer()

@router.callback_query(fabrics.ThemePagination.filter(F.action.in_(["prev", "next"])))
async def theme_pagination_handler(call: CallbackQuery, callback_data: fabrics.Pagination):
    theme_or_topic = callback_data.theme_or_topic
    table = callback_data.db_table
    group_subject = callback_data.db_group_subject
    if theme_or_topic == 'theme':
        btns = await theme_from_topic(table, group_subject)
        buttons = [btns[i:i + 10] for i in range(0, len(btns), 10)]
    elif theme_or_topic == 'topic':
        btns = await topic_from_table(table)
        buttons = [btns[i:i + 10] for i in range(0, len(btns), 10)]
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(buttons) - 1) else page_num

    # Создаем экземпляр функции paginator с конкретными значениями db_table и db_theme
    my_paginator = await create_theme_paginator(db_table=table, db_group_subject=group_subject, theme_or_topic=theme_or_topic)

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
        "Оберіть тему",
            reply_markup=my_paginator(page)
        )
    await call.answer()






