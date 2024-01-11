from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Смайлики'),
            KeyboardButton(text='Ссылки')
        ],
        [
            KeyboardButton(text='Калькулятор'),
            KeyboardButton(text='Спец кнопки')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите действие из меню',
    selective=True
)

linsk_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="YouTube", url='https://www.youtube.com/watch?v=zA52uNzx7Y4&ab_channel=malawolf85'),
            InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=mmmurkaa")
        ]
    ]

)

spec_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправить гео', request_location=True),
            KeyboardButton(text='Отправить контакт', request_contact=True)
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True
)

class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def paginator(page: int=0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text="➡️", callback_data=Pagination(action="next", page=page).pack()),
        width=2
    )
    return builder.as_markup()
def calc_kb():
    items = [
        '1', '2', '3', '/',
        '4', '5', '6', '*',
        '7', '8', '9', '-',
        '0', '.', '=', '+',
    ]

    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.button(text='Назад')
    builder.adjust(*[4] * 4)

    return builder.as_markup(resize_keyboard=True)