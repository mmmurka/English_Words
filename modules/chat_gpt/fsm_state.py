from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import StateFilter
from modules.chat_gpt.chat_api import ChatGPT
from aiogram.types import CallbackQuery

router = Router()
chat_gpt = ChatGPT()


class ChatGPTState(StatesGroup):
    waiting_for_message = State()


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text("Ваш профіль")
    await callback.message.reply("Hello, I your english teacher!")
    await state.set_state(ChatGPTState.waiting_for_message)


@router.message(StateFilter(ChatGPTState.waiting_for_message), F.content_type == types.ContentType.TEXT)
async def chat_with_gpt(message: types.Message, state: FSMContext):
    user_message = message.text

    # Получаем ответ от ChatGPT
    gpt_reply = await chat_gpt.get_response(user_message)

    # Отправляем ответ пользователю
    await message.reply(gpt_reply)

    # Оставляем состояние ожидания текстового сообщения
    await state.set_state(ChatGPTState.waiting_for_message)
