from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

developers_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Nemsh", url="tg://resolve?domain=sliznyachok"),
            InlineKeyboardButton(text="mmmurka", url="tg://resolve?domain=mmmurkaa"),
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ],
    resize_keyboard=True,
)

back_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]],
    resize_keyboard=True,
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back"),
        ],
    ],
)

translate_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="translate_api"),
            InlineKeyboardButton(text="Переклад", callback_data="ukraine"),
        ]
    ],
    resize_keyboard=True,
)

translate = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="translate_api"),
            InlineKeyboardButton(text="Переклад", callback_data="english"),
        ]
    ],
    resize_keyboard=True,
)
