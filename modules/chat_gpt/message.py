from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from modules.chat_gpt.chat_api import ChatGPT
from modules.chat_gpt.states import ChatGPTState
from modules.chat_gpt.inline_keyboard import keyboard_uk
from aiogram import F, Router
from contextlib import suppress

router = Router()
Chat_gpt = ChatGPT()


@router.message(StateFilter(ChatGPTState.waiting_for_message), F.content_type == types.ContentType.TEXT)
async def chat_with_gpt(message: types.Message, state: FSMContext):
    user_message = message.text

    data = await state.get_data()
    previous_message_id = data.get("previous_message_id")

    if previous_message_id:
        with suppress(TelegramBadRequest):
            await message.bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=previous_message_id,
                                                        reply_markup=None)

    gpt_reply = await Chat_gpt.get_response(user_message)

    await state.update_data(gpt_reply=gpt_reply)

    sent_message = await message.reply(gpt_reply, reply_markup=keyboard_uk)

    await state.update_data(previous_message_id=sent_message.message_id)

    await state.set_state(ChatGPTState.waiting_for_message)
