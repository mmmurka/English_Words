from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

linsk_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="YouTube",
                                 url='https://www.youtube.com/watch?v=zA52uNzx7Y4&ab_channel=malawolf85'),
            InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=mmmurkaa")
        ]
    ]

)
