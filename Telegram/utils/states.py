from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()
    sex = State()
    about = State()
    photo = State()