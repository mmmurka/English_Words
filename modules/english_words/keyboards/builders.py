from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


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
