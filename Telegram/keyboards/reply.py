from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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