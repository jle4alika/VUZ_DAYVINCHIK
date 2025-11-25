from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ContentType, Contact
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import database.requests.users as users

import keyboards.reply_keyboards.main as kbr
from utils.user_profile import user_profile

router = Router()


@router.message(F.text == "3")
async def no_anytime_search(message: Message):
    await message.answer(
        "Так ты не узнаешь, что кому-то нравишься... Точно хочешь отключить свою анкету?",
        reply_markup=kbr.delete_me,
    )


@router.message(F.text == "😴 Отключить анкету")
async def delete_me(message: Message):
    await message.answer(
        "Надеюсь ты нашел кого-то благодаря мне! Рад был с тобой пообщаться, будет скучно – пиши, обязательно найдем тебе кого-нибудь",
        reply_markup=kbr.return_me,
    )


@router.message(F.text == "← Назад")
async def back_to_main_menu(message: Message):
    media = await user_profile(message.from_user.id)
    await message.answer("Так выглядит твоя анкета:")
    await message.answer_media_group(media)
    await message.answer(
        """1. Смотреть анкеты.
2. Заполнить анкету заново.
3. Изменить фото/видео.
4. Изменить текст анкеты.""",
        reply_markup=kbr.my_profile,
    )


@router.message(F.text == "🚀 Смотреть анкеты")
async def back_to_main_menu(message: Message):
    media = await user_profile(message.from_user.id)
    await message.answer("Так выглядит твоя анкета:")
    await message.answer_media_group(media)
    await message.answer(
        """1. Смотреть анкеты.
2. Заполнить анкету заново.
3. Изменить фото/видео.
4. Изменить текст анкеты.""",
        reply_markup=kbr.my_profile,
    )
