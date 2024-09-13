from aiogram.fsm.state import State, StatesGroup


class ChatGPTState(StatesGroup):
    waiting_for_message = State()
