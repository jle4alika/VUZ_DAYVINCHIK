from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


my_gender = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Я девушка", callback_data="g_female")],
        [InlineKeyboardButton(text="Я парень", callback_data="g_male")],
    ]
)
