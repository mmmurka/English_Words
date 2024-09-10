from contextlib import suppress

from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import StateFilter
from modules.chat_gpt.chat_api import ChatGPT
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from layers.translate_api.translateAPI import trans_text


router = Router()
Chat_gpt = ChatGPT()


class ChatGPTState(StatesGroup):
    waiting_for_message = State()


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text("Ваш профіль")
    await callback.message.reply("nemsh gavnoed!")
    await state.set_state(ChatGPTState.waiting_for_message)


@router.message(StateFilter(ChatGPTState.waiting_for_message), F.content_type == types.ContentType.TEXT)
async def chat_with_gpt(message: types.Message, state: FSMContext):
    user_message = message.text

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перевести", callback_data="translate")]
    ])
    # Получаем ответ от ChatGPT
    global gpt_reply
    gpt_reply = await Chat_gpt.get_response(user_message)

    # Отправляем ответ пользователю
    await message.reply(gpt_reply, reply_markup=keyboard)

    # Оставляем состояние ожидания текстового сообщения
    await state.set_state(ChatGPTState.waiting_for_message)


@router.callback_query(F.data == "translate")
async def button_translate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    original_text = data.get("gpt_reply")

    translated_text = await trans_text(text=original_text, src='en', dest='uk')

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(translated_text)
    await callback.answer()
