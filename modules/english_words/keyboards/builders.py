from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from modules.words.keyboards.paginators import Pagination

def topic_kb(topics: list, table: str):

    keyboard = InlineKeyboardBuilder()
    for topic in topics:
        keyboard.button(text=topic, callback_data=f'theme:{table}:{topic}')
    keyboard.button(text='Назад', callback_data='topics')
    keyboard.adjust(1)

    return keyboard.as_markup()


def theme_kb(themes: list, table: str, group_subject: str):

    keyboard = InlineKeyboardBuilder()
    for theme in themes:
        theme_word = theme.split(' - ')[1]
        if len(theme_word) > 20:
            theme_word = theme_word[:20]
        end = '_'.join(theme_word.split())
        keyboard.button(text=theme, callback_data=f'words:{table}:{end}')
    keyboard.button(text='Назад', callback_data=f'topic:{table}:{group_subject}')
    keyboard.adjust(1)

    return keyboard.as_markup()

