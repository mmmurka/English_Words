from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_en = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇸", callback_data="translate_to_en")]
    ])

keyboard_uk = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇦", callback_data="translate_to_uk")]
    ])
