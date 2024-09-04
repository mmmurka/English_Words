from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from layers.functions.cb_encoder import encode_table

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


def word_tables_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='English By Level', callback_data=f'group_subject:{encode_table('english_by_level')}'),
        InlineKeyboardButton(text='Verbs', callback_data=f'group_subject:{encode_table('verbs')}'),
        InlineKeyboardButton(text='Topic Vocabulary', callback_data=f'group_subject:{encode_table('topic_vocabulary')}'),
        InlineKeyboardButton(text='Adverbs', callback_data=f'group_subject:{encode_table('adverbs')}'),
        InlineKeyboardButton(text='Collocations', callback_data=f'group_subject:{encode_table('collocations')}'),
        InlineKeyboardButton(text='Adjectives', callback_data=f'group_subject:{encode_table('adjectives')}'),
        InlineKeyboardButton(text='Most Common', callback_data=f'group_subject:{encode_table('most_common')}'),
        InlineKeyboardButton(text='IELTS', callback_data=f'group_subject:{encode_table('ielts')}'),
        InlineKeyboardButton(text='Назад', callback_data='back'),
        width=2)
    return builder.as_markup()


def greeting_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Теми', callback_data='word_tables'),
        InlineKeyboardButton(text='Розробники', callback_data='developers'),
        InlineKeyboardButton(text='Профіль', callback_data='profile'),
        width=2
    )
    return builder.as_markup()

