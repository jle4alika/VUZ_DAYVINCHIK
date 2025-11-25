import asyncio

from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ContentType, Contact, PhotoSize, Video, FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import database.requests.users as users

import keyboards.reply_keyboards.main as kbr
from utils.coordinates import resolve_city
from utils.user_profile import save_file, user_profile

router = Router()


class States(StatesGroup):
    zzz_action = State()
    action = State()


@router.message(F.text == "1 👍")
async def my_likes(message: Message, state: FSMContext):
    likes = await users.get_user_unchecked_likes(message.from_user.id)

    if not likes:
        await message.answer("Вас никто не лайкнул")
        await message.answer(
            """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
            reply_markup=kbr.main,
        )
        return

    like = likes[0]
    index = 0
    await state.update_data(likes=likes, like=like, index=index)

    if len(likes) - 1 >= index:
        index += 1

        like = likes[index]

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(like, message.from_user.id)
        await message.answer_media_group(media)

        message_to_user = await users.message_to_user(like, message.from_user.id)
        if message_to_user:
            if not message_to_user.file:
                await message.answer(f"Сообщение для тебя: {message_to_user.text}")
            else:
                await message.answer_video(
                    video=FSInputFile(message_to_user.file),
                    caption="Сообщение для тебя",
                )

        await state.set_state(States.action)
    else:
        await message.answer("Анкеты закончились :(")
        await message.answer(
            """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
            reply_markup=kbr.main,
        )


@router.message(States.action, F.text == "❤️")
async def like_my_like(message: Message, state: FSMContext):
    data = await state.get_data()
    likes = data.get("likes")
    like = data.get("like")
    index = data.get("index")

    like_user = await users.get_user(like)

    await users.create_like(message.from_user.id, like)
    await users.like_checked(like, message.from_user.id)
    await users.like_checked(message.from_user.id, like)
    link = f'<a href="https://t.me/{like_user.username}?text="Привет! Я с Друзья СурГУ ✨"">{like_user.name}</a>'

    print(link)
    await message.answer(
        f"""Отлично! Надеюсь вы хорошо проведёте время 🙌

Начинай общаться 👉 {link}""",
        parse_mode=ParseMode.HTML,
    )
    await asyncio.sleep(2)

    if len(likes) - 1 >= index:
        index += 1
        like = likes[index]
        await state.update_data(like=like, index=index)

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(like, message.from_user.id)
        await message.answer_media_group(media)

        message_to_user = await users.message_to_user(like, message.from_user.id)
        if message_to_user:
            if not message_to_user.file:
                await message.answer(f"Сообщение для тебя: {message_to_user.text}")
            else:
                await message.answer_video(
                    video=FSInputFile(message_to_user.file),
                    caption="Сообщение для тебя",
                )
        await state.set_state(States.action)

    else:
        await message.answer("Анкеты закончились :(")
        await message.answer(
            """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
            reply_markup=kbr.main,
        )


@router.message(States.action, F.text == "👎")
async def dislike_my_like(message: Message, state: FSMContext):
    data = await state.get_data()
    likes = data.get("likes")
    like = data.get("like")
    index = data.get("index")

    await users.create_dislike(message.from_user.id, like)

    if len(likes) - 1 >= index:
        index += 1
        like = likes[index]
        await state.update_data(like=like, index=index)

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(like, message.from_user.id)
        await message.answer_media_group(media)

        message_to_user = await users.message_to_user(like, message.from_user.id)
        if message_to_user:
            if not message_to_user.file:
                await message.answer(f"Сообщение для тебя: {message_to_user.text}")
            else:
                await message.answer_video(
                    video=FSInputFile(message_to_user.file),
                    caption="Сообщение для тебя",
                )
        await state.set_state(States.action)
    else:
        await message.answer("Анкеты закончились :( попробуйте позже")
        await message.answer(
            """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
            reply_markup=kbr.main,
        )


@router.message(F.text == "2 💤")
async def my_likes(message: Message, state: FSMContext):
    await message.answer(
        "Так ты не узнаешь, что кому-то нравишься... Точно хочешь отключить свою анкету?",
        reply_markup=kbr.delete_me,
    )
    await state.set_state(States.zzz_action)


@router.message(States.zzz_action)
async def zzz(message: Message, state: FSMContext):
    await state.clear()

    if message.text == "← Назад":
        await message.delete()
        return
