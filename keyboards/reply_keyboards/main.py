from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

start = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="👌 давай начнем")]],
    resize_keyboard=True,
)

okay = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="👌 Ok")]],
    resize_keyboard=True,
)


# --- Клавиатура для выбора пола ---
my_gender = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Я парень")], [KeyboardButton(text="Я девушка")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# --- Клавиатура для выбора интереса ---
interest_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Девушки")],
        [KeyboardButton(text="Парни")],
        [KeyboardButton(text="Всё равно")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# --- Клавиатура для отправки геолокации ---
location_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отправить геолокацию", request_location=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# --- Клавиатура для отправки номера телефона ---
send_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить мой номер телефона", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# --- Клавиатура "Пропустить" для описания ---
skip_description_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Пропустить")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

add_photo_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Это всё, сохранить фото")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# --- Клавиатура подтверждения анкеты ---
confirm_profile_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет, заполнить заново")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


search = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❤️"),
            KeyboardButton(text="💌 / 📹"),
            KeyboardButton(text="👎"),
            KeyboardButton(text="💤"),
        ]
    ],
    resize_keyboard=True,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1 🚀"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
        ]
    ],
    resize_keyboard=True,
)


my_profile = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1 🚀"),
            KeyboardButton(text="2"),
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
        ]
    ],
    resize_keyboard=True,
)

back_profile = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Вернуться назад")]],
    resize_keyboard=True,
)

back_photos = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Вернуться назад")],
        [KeyboardButton(text="Это всё, сохранить фото")],
    ],
    resize_keyboard=True,
)

delete_me = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="😴 Отключить анкету")],
        [KeyboardButton(text="← Назад")],
    ],
    resize_keyboard=True,
)

return_me = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Смотреть анкеты")]],
    resize_keyboard=True,
)


check_likes = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="1 👍"), KeyboardButton(text="2 💤")]],
    resize_keyboard=True,
)


check_like = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❤️"),
            KeyboardButton(text="👎"),
            KeyboardButton(text="💤"),
        ]
    ],
    resize_keyboard=True,
)
