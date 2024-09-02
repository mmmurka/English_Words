from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

developers_kb = InlineKeyboardMarkup(
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

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='back'),
        ],
    ],
)


def group_subject_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='English By Level', callback_data='topic:english_by_level'),
        InlineKeyboardButton(text='Verbs', callback_data='topic:verbs'),
        InlineKeyboardButton(text='Topic Vocabulary', callback_data='topic:topic_vocabulary'),
        InlineKeyboardButton(text='Adverbs', callback_data='topic:adverbs'),
        InlineKeyboardButton(text='Collocations', callback_data='topic:collocations'),
        InlineKeyboardButton(text='Adjectives', callback_data='topic:adjectives'),
        InlineKeyboardButton(text='Most Common', callback_data='topic:most_common'),
        InlineKeyboardButton(text='IELTS', callback_data='topic:ielts'),
        InlineKeyboardButton(text='Назад', callback_data='back'),
        width=2)
    return builder.as_markup()


def greeting_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Теми', callback_data='group_subject'),
        InlineKeyboardButton(text='Розробники', callback_data='developers'),
        InlineKeyboardButton(text='Профіль', callback_data='profile'),
        width=2
    )
    return builder.as_markup()


