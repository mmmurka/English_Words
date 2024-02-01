from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Telegram.translate.translateAPI import trans_text
import asyncio


# async def user_translation():
#     user_input = input("Введите текст для перевода: ")
#     result = await trans_text(text=user_input, src='uk', dest='en')
#     print(result)
#
# asyncio.run(user_translation())


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


def profile(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, list):
        [builder.button(text=txt) for txt in text]
    elif isinstance(text, str):
        builder.button(text=text)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def topic_kb(text: list):

    keyboard = InlineKeyboardBuilder()
    for txt in text:
        keyboard.button(text=txt, callback_data=txt)
    keyboard.button(text='Назад', callback_data='topics')
    keyboard.adjust(1)

    return keyboard.as_markup()
