from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    word = State()
    slovo = State()

