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

back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='back')
        ]
    ],
    resize_keyboard=True
)

translate_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='back'),
            InlineKeyboardButton(text='Переклад', callback_data='translate')
        ]
    ],
    resize_keyboard=True
)

topics_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='English By Level', callback_data='topics'),
            InlineKeyboardButton(text='Verbs', callback_data='topics'),

        ],
        [
            InlineKeyboardButton(text='Topic Vocabulary', callback_data='topics'),
            InlineKeyboardButton(text='Adverbs', callback_data='topics'),
        ],
        [

            InlineKeyboardButton(text='Collocations', callback_data='topics'),
            InlineKeyboardButton(text='Adjectives', callback_data='topics'),
        ],
        [
            InlineKeyboardButton(text='Most Common', callback_data='topics'),
            InlineKeyboardButton(text='IELTS', callback_data='topics'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='back'),
        ]

    ],
    resize_keyboard=True
)
