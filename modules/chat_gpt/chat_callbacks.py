from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from modules.chat_gpt.states import ChatGPTState
from aiogram import Router, F
from modules.chat_gpt.chat_api import ChatGPT
from aiogram.types import CallbackQuery
from layers.translate_api.translateAPI import trans_text
from modules.chat_gpt.inline_keyboard import keyboard_en, keyboard_uk, keyboard_main

router = Router()
Chat_gpt = ChatGPT()


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Оберіть необхідний пункт:", reply_markup=keyboard_main)


@router.callback_query(F.data == "translate_to_uk")
async def button_translate_to_uk(callback: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    gpt_reply: str = data.get("gpt_reply", "")

    if gpt_reply:
        translated_text: str | Exception = await trans_text(text=gpt_reply, src='en', dest='uk')

        with suppress(TelegramBadRequest):
            await callback.message.edit_text(translated_text, reply_markup=keyboard_en)
        await callback.answer()
    else:
        await callback.answer("Немає тексту для перекладу", show_alert=True)


@router.callback_query(F.data == "translate_to_en")
async def button_translate_to_en(callback: CallbackQuery, state: FSMContext):
    data: dict = await state.get_data()
    gpt_reply: str = data.get("gpt_reply", "")
    translated_text: str | Exception = await trans_text(text=gpt_reply, src='uk', dest='en')

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(translated_text, reply_markup=keyboard_uk)
    await callback.answer()


@router.callback_query(F.data == "test_english_level")
async def test_english_level(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Тест рівня англійської 🇺🇸", reply_markup=keyboard_main)
