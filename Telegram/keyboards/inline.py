from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


linsk_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Nemsh",
                                 url='tg://resolve?domain=sliznyachok'),
            InlineKeyboardButton(text="mmmurka", url="tg://resolve?domain=mmmurkaa")
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='back')
        ],

    ],


 resize_keyboard=True
)

