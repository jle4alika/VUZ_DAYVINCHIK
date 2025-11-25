import database.requests.users as users
import os
from aiogram import Bot
from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile


async def save_file(file, user_id: int, bot: Bot) -> str:
    """
    Скачивает файл в files/<user_id>/ и возвращает полный путь.
    """
    folder = f"files/{user_id}"
    os.makedirs(folder, exist_ok=True)

    file_info = await bot.get_file(file.file_id)
    file_ext = file_info.file_path.split(".")[-1]
    local_path = f"{folder}/{file.file_id}.{file_ext}"

    await bot.download_file(file_info.file_path, local_path)
    return os.path.abspath(local_path)


async def user_profile(tg_id: int, to_user_tg_id: int = None):
    media = []
    user = await users.get_user(tg_id)
    city = user.city_name
    name = user.name
    age = user.age
    about = " - " + user.about if user.about else ""

    caption = f"""{name}, {age}, {city}{about}"""

    file_paths = user.files.split(",")

    for i, path in enumerate(file_paths):
        ext = os.path.splitext(path.lower())[1]
        print(ext)
        if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            media.append(
                InputMediaPhoto(
                    media=FSInputFile(path) if os.path.exists(path) else path
                )
            )
        elif ext in {".mp4", ".avi", ".mov", ".mkv"}:
            media.append(
                InputMediaVideo(
                    media=FSInputFile(path) if os.path.exists(path) else path
                )
            )
        else:
            print(f"⚠️ Пропущен неподдерживаемый файл: {path}")

    media[0].caption = caption

    return media


def plural_form(n):
    forms = ["человеку", "людям", "людям"]

    n = abs(n)
    if 11 <= n % 100 <= 19:
        return forms[2]
    elif n % 10 == 1:
        return forms[0]
    elif 2 <= n % 10 <= 4:
        return forms[1]
    else:
        return forms[2]
