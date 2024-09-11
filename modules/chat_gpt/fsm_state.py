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
    await callback.message.edit_text("Почни спілкування з вчителем прямо зараз!")
    await state.set_state(ChatGPTState.waiting_for_message)


@router.message(StateFilter(ChatGPTState.waiting_for_message), F.content_type == types.ContentType.TEXT)
async def chat_with_gpt(message: types.Message, state: FSMContext):
    user_message = message.text

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇦", callback_data="translate")]
    ])
    gpt_reply = await Chat_gpt.get_response(user_message)

    await state.update_data(gpt_reply=gpt_reply)

    await message.reply(gpt_reply, reply_markup=keyboard)
    await state.set_state(ChatGPTState.waiting_for_message)


@router.callback_query(F.data == "translate")
async def button_translate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    gpt_reply = data.get("gpt_reply", "")

    if gpt_reply:
        translated_text = await trans_text(text=gpt_reply, src='en', dest='uk')

        with suppress(TelegramBadRequest):
            await callback.message.edit_text(translated_text)
        await callback.answer()
    else:
        await callback.answer("No text to translate", show_alert=True)
