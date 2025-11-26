import asyncio

from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ContentType, Contact, FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import database.requests.users as users

import keyboards.reply_keyboards.main as kbr
from utils.coordinates import resolve_city
from utils.user_profile import user_profile, save_file, plural_form

router = Router()


class SearchStates(StatesGroup):
    questionnaires = State()
    questionnaire = State()

    index = State()
    message = State()


class States(StatesGroup):
    zzz_action = State()
    action = State()


@router.message(States.action, F.text == "❤️")
async def like_my_like(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    questionnaires = data.get("questionnaires")
    questionnaire = data.get("questionnaire")
    index = data.get("index")

    like_user = await users.get_user(questionnaire)

    await users.create_like(message.from_user.id, questionnaire)
    await users.like_checked(questionnaire, message.from_user.id)

    await bot.send_message(
        questionnaire, "Вас лайкнули! Скорее смотри кто это в Главном меню"
    )
    link = f'<a href="https://t.me/{like_user.username}?text=Привет! Я с Друзья СурГУ ✨">{like_user.name}</a>'

    await message.answer(
        f"""Отлично! Надеюсь вы хорошо проведёте время 🙌

Начинай общаться 👉 {link}""",
        parse_mode=ParseMode.HTML,
    )
    await asyncio.sleep(2)

    if index >= 1:
        index -= 1
        questionnaire = questionnaires[index]
        await state.update_data(questionnaire=questionnaire, index=index)

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(questionnaire, message.from_user.id)
        await message.answer_media_group(media)

        message_to_user = await users.message_to_user(
            questionnaire, message.from_user.id
        )
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
    questionnaires = data.get("questionnaires")
    questionnaire = data.get("questionnaire")
    index = data.get("index")

    await users.create_dislike(message.from_user.id, questionnaire)

    if index >= 1:
        index -= 1
        questionnaire = questionnaires[index]
        await state.update_data(questionnaire=questionnaire, index=index)

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(questionnaire, message.from_user.id)
        await message.answer_media_group(media)

        message_to_user = await users.message_to_user(
            questionnaire, message.from_user.id
        )
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


@router.message(F.text == "💤")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Подождем пока кто-то увидит твою анкету")
    await message.answer(
        """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
        reply_markup=kbr.main,
    )


@router.message(F.text == "1 🚀")
async def search(message: Message, state: FSMContext):
    questionnaires = await users.get_user_unchecked_likes(message.from_user.id)
    print(questionnaires)

    if questionnaires:
        questionnaire = questionnaires[-1]
        index = len(questionnaires) - 1
        await state.update_data(
            questionnaires=questionnaires, questionnaire=questionnaire, index=index
        )

        await message.answer("Твои лайки:")

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(questionnaire, message.from_user.id)
        await message.answer_media_group(media)

        message_to_user = await users.message_to_user(
            questionnaire, message.from_user.id
        )
        if message_to_user:
            if not message_to_user.file:
                await message.answer(f"Сообщение для тебя: {message_to_user.text}")
            else:
                await message.answer_video(
                    video=FSInputFile(message_to_user.file),
                    caption="Сообщение для тебя",
                )

        await state.set_state(States.action)
        return

    questionnaires = await users.search(message.from_user.id)
    if questionnaires:
        questionnaire = questionnaires[-1]
        await state.update_data(
            questionnaires=questionnaires,
            questionnaire=questionnaire,
            index=len(questionnaires) - 1,
        )

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(questionnaire, message.from_user.id)
        await message.answer_media_group(media)
    else:
        questionnaires = await users.get_user_unchecked_likes(message.from_user.id)

        if not questionnaires:
            await message.answer("Анкеты закончились :( попробуйте позже")
            await message.answer(
                """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
                reply_markup=kbr.main,
            )
        if questionnaires:
            word = plural_form(len(questionnaires))
            await message.answer("Анкеты закончились :( попробуйте позже")
            await message.answer(
                f"""Ты понравился {len(questionnaires)} {word}, показать их?

1. Показать.
2. Не хочу больше никого смотреть.""",
                reply_markup=kbr.main,
            )


@router.message(F.text == "❤️")
async def questionnaire(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    questionnaires = data.get("questionnaires")
    questionnaire = data.get("questionnaire")
    index = data.get("index")

    await users.create_like(message.from_user.id, questionnaire)

    if index >= 1:
        index -= 1

        questionnaire = questionnaires[index]
        await state.update_data(questionnaire=questionnaire, index=index)

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(questionnaire, message.from_user.id)
        await message.answer_media_group(media)
    else:
        questionnaires = await users.get_user_unchecked_likes(message.from_user.id)

        if not questionnaires:
            await message.answer("Анкеты закончились :( попробуйте позже")
            await message.answer(
                """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
                reply_markup=kbr.main,
            )
        if questionnaires:
            word = plural_form(len(questionnaires))
            await message.answer("Анкеты закончились :( попробуйте позже")
            await message.answer(
                f"""Ты понравился {len(questionnaires)} {word}, показать их?

1. Показать.
2. Не хочу больше никого смотреть.""",
                reply_markup=kbr.main,
            )


@router.message(F.text == "💌 / 📹")
async def message_to_user(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        """Напиши сообщение для этого пользователя

или запиши короткое видео(до 15сек)""",
        reply_markup=kbr.back_profile,
    )
    await state.set_state(SearchStates.message)


@router.message(SearchStates.message, F.text)
async def new_message(message: Message, state: FSMContext):
    data = await state.get_data()
    questionnaires = data.get("questionnaires")
    questionnaire = data.get("questionnaire")
    index = data.get("index")

    if message.text != "Вернуться назад":
        await users.create_message(message.from_user.id, questionnaire, message.text)
    if index >= 1:
        index -= 1

        questionnaire = questionnaires[index]
        await state.update_data(questionnaire=questionnaire, index=index)

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(questionnaire, message.from_user.id)
        await message.answer_media_group(media)
    else:
        questionnaires = await users.get_user_unchecked_likes(message.from_user.id)

        if not questionnaires:
            await message.answer("Анкеты закончились :( попробуйте позже")
            await message.answer(
                """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
                reply_markup=kbr.main,
            )
        if questionnaires:
            word = plural_form(len(questionnaires))
            await message.answer("Анкеты закончились :( попробуйте позже")
            await message.answer(
                f"""Ты понравился {len(questionnaires)} {word}, показать их?

1. Показать.
2. Не хочу больше никого смотреть.""",
                reply_markup=kbr.main,
            )


@router.message(SearchStates.message, F.video)
async def reg_media(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    questionnaires = data.get("questionnaires")
    questionnaire = data.get("questionnaire")
    index = data.get("index")

    file = message.video

    try:
        # Сохраняем файл
        file_path = await save_file(file, message.from_user.id, bot)
        await users.create_message(message.from_user.id, questionnaire, "", file_path)
        await users.create_like(message.from_user.id, questionnaire)

        if index >= 1:
            index -= 1
            questionnaire = questionnaires[index]
            await state.update_data(questionnaire=questionnaire, index=index)

            await message.answer("✨🔍", reply_markup=kbr.search)
            media = await user_profile(questionnaire, message.from_user.id)
            await message.answer_media_group(media)
        else:
            questionnaires = await users.get_user_unchecked_likes(message.from_user.id)

            if not questionnaires:
                await message.answer("Анкеты закончились :( попробуйте позже")
                await message.answer(
                    """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
                    reply_markup=kbr.main,
                )
            if questionnaires:
                word = plural_form(len(questionnaires))
                await message.answer("Анкеты закончились :( попробуйте позже")
                await message.answer(
                    f"""Ты понравился {len(questionnaires)} {word}, показать их?

            1. Показать.
            2. Не хочу больше никого смотреть.""",
                    reply_markup=kbr.main,
                )

    except Exception as e:
        await message.answer("Ошибка при сохранении медиа. Попробуй еще раз.")


@router.message(F.text == "👎")
async def dislike(message: Message, state: FSMContext):
    data = await state.get_data()
    questionnaires = data.get("questionnaires")
    questionnaire = data.get("questionnaire")
    index = data.get("index")

    await users.create_dislike(message.from_user.id, questionnaire)

    if index >= 1:
        index -= 1

        questionnaire = questionnaires[index]
        await state.update_data(questionnaire=questionnaire, index=index)

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(questionnaire, message.from_user.id)
        await message.answer_media_group(media)
    else:
        questionnaires = await users.get_user_unchecked_likes(message.from_user.id)

        if not questionnaires:
            await message.answer("Анкеты закончились :( попробуйте позже")
            await message.answer(
                """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
                reply_markup=kbr.main,
            )
        if questionnaires:
            word = plural_form(len(questionnaires))
            await message.answer("Анкеты закончились :( попробуйте позже")
            await message.answer(
                f"""Ты понравился {len(questionnaires)} {word}, показать их?

1. Показать.
2. Не хочу больше никого смотреть.""",
                reply_markup=kbr.main,
            )


@router.message(F.text == "1 👍")
async def my_likes(message: Message, state: FSMContext):
    questionnaires = await users.get_user_unchecked_likes(message.from_user.id)

    if not questionnaires:
        await message.answer("Вас никто не лайкнул")
        await message.answer(
            """1. Смотреть анкеты.
2. Моя анкета.
3. Я больше не хочу никого искать.""",
            reply_markup=kbr.main,
        )
        return

    questionnaire = questionnaires[-1]
    index = len(questionnaires) - 1
    await state.update_data(
        questionnaires=questionnaires, questionnaire=questionnaire, index=index
    )

    if index >= 1:
        index -= 1

        questionnaire = questionnaires[index]

        await message.answer("✨🔍", reply_markup=kbr.search)
        media = await user_profile(questionnaire, message.from_user.id)
        await message.answer_media_group(media)

        message_to_user = await users.message_to_user(
            questionnaire, message.from_user.id
        )
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
