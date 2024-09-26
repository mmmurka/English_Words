from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇸", callback_data="translate_to_en")]
    ])

keyboard_uk = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇦", callback_data="translate_to_uk")]
    ])

keyboard_main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Тест рівня англійської 🇺🇸", callback_data="test_english_level"),
    ],
    [
        InlineKeyboardButton(text="Present Simple", callback_data="future"),
    ],
    [
        InlineKeyboardButton(text="Past Simple", callback_data="future"),
    ],
    [
        InlineKeyboardButton(text="Present Perfect", callback_data="future"),
    ],
    [
        InlineKeyboardButton(text="Back", callback_data="back"),
    ]
])
