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
            InlineKeyboardButton(text='Назад', callback_data='translate_api'),
            InlineKeyboardButton(text='Переклад', callback_data='ukraine')
        ]
    ],
    resize_keyboard=True
)
translate = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='translate_api'),
            InlineKeyboardButton(text='Переклад', callback_data='english')
        ]
    ],
    resize_keyboard=True
)

trans_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇺🇦 -> 🇺🇸', callback_data='english'),
            InlineKeyboardButton(text='🇺🇸 -> 🇺🇦', callback_data='ukraine')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='back')
        ]
    ]
)

topics_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='English By Level', callback_data='topic:english_by_level'),
            InlineKeyboardButton(text='Verbs', callback_data='topic:verbs'),
        ],
        [
            InlineKeyboardButton(text='Topic Vocabulary', callback_data='topic:topic_vocabulary'),
            InlineKeyboardButton(text='Adverbs', callback_data='topic:adverbs'),
        ],
        [
            InlineKeyboardButton(text='Collocations', callback_data='topic:collocations'),
            InlineKeyboardButton(text='Adjectives', callback_data='topic:adjectives'),
        ],
        [
            InlineKeyboardButton(text='Most Common', callback_data='topic:most_common'),
            InlineKeyboardButton(text='IELTS', callback_data='topic:ielts'),
        ],

        [
            InlineKeyboardButton(text='Назад', callback_data='back'),
        ]

    ],
    resize_keyboard=True
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='back'),
        ],
    ],
)
