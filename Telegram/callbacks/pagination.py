from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from Telegram.keyboards import fabrics
from Telegram.data.subloader import get_json
from Telegram.callbacks.topics import words_from_theme
from Telegram.keyboards.fabrics import create_paginator
router = Router()


@router.callback_query(fabrics.Pagination.filter(F.action.in_(["prev", "next"])))
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