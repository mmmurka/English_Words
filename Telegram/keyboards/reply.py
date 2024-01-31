from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='243'),
            KeyboardButton(text='Автори')
        ],
        [
            KeyboardButton(text='Калькулятор'),
            KeyboardButton(text='Спец кнопки')
        ]
    ],
    resize_keyboard=True, # адаптація клавіатури до розмірів екрану
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

rmk_kb = ReplyKeyboardRemove()
