from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ContentType, Contact
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import database.requests.users as users

import keyboards.reply_keyboards.main as kbr
from utils.coordinates import resolve_city
from utils.user_profile import user_profile, save_file

router = Router()


class ProfileStates(StatesGroup):
    action = State()
    change_text = State()
    change_media = State()


@router.message(F.text == "Вернуться назад")
async def back_to_profile(message: Message, state: FSMContext):
    media = await user_profile(message.from_user.id)
    await message.answer("Так выглядит твоя анкета:", reply_markup=kbr.my_profile)
    await message.answer_media_group(media)
    await message.answer(
        """1. Смотреть анкеты.
2. Заполнить анкету заново.
3. Изменить фото/видео.
4. Изменить текст анкеты.""",
        reply_markup=kbr.my_profile,
    )
    await state.set_state(ProfileStates.action)


@router.message(ProfileStates.action, F.text == "2")
async def registrate_again(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ваша прошлая анкета будет удалена", reply_markup=kbr.okay)


@router.message(F.text == "2")
async def my_profile(message: Message, state: FSMContext):
    media = await user_profile(message.from_user.id)
    await message.answer("Так выглядит твоя анкета:", reply_markup=kbr.my_profile)
    await message.answer_media_group(media)
    await message.answer(
        """1. Смотреть анкеты.
2. Заполнить анкету заново.
3. Изменить фото/видео.
4. Изменить текст анкеты.""",
        reply_markup=kbr.my_profile,
    )
    await state.set_state(ProfileStates.action)


@router.message(ProfileStates.action, F.text == "3")
async def change_media(message: Message, state: FSMContext):
    await state.update_data(media_list=[], current_media_count=0)
    await state.set_state(ProfileStates.change_media)
    await message.answer(
        "Теперь пришли фото или запиши видео 👍 (до 15 сек), его будут видеть другие пользователи"
    )


@router.message(ProfileStates.change_media, F.photo | F.video)
async def reg_media(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    current_media_count = data.get("current_media_count", 0)

    if current_media_count >= 3:
        await message.answer(
            "Достигнут лимит в 3 медиафайла. Отправь 'Это всё, сохранить фото', чтобы завершить."
        )
        return

    # Получаем файл (фото или видео)
    if message.photo:
        file = message.photo[-1]
    elif message.video:
        file = message.video
    else:
        return

    try:
        # Сохраняем файл
        file_path = await save_file(file, message.from_user.id, bot)

        # Получаем текущий список медиа
        media_list = data.get("media_list", [])
        media_list.append(file_path)

        current_media_count += 1

        await state.update_data(
            media_list=media_list, current_media_count=current_media_count
        )

        await message.answer(
            f"Фото добавлено – {current_media_count} из 3. Еще одно?",
            reply_markup=kbr.add_photo_kb,
        )

    except Exception as e:
        await message.answer("Ошибка при сохранении медиа. Попробуй еще раз.")


@router.message(ProfileStates.change_media, F.text == "Это всё, сохранить фото")
async def finish_media_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    media_list = data.get("media_list", [])

    if not media_list:
        await message.answer(
            "Ты не добавил ни одного медиа. Отправь фото или видео сначала."
        )
        return

    # Сохраняем все пути через запятую
    media_paths_str = ",".join(media_list)
    await state.update_data(media=media_paths_str)

    # Здесь можно сохранить в базу данных
    await users.set_user_files(message.from_user.id, media_paths_str)

    print(
        f"Сохраненные медиа для пользователя {message.from_user.id}: {media_paths_str}"
    )
    media = await user_profile(message.from_user.id)
    await message.answer("Так выглядит твоя анкета:", reply_markup=kbr.my_profile)
    await message.answer_media_group(media)
    await message.answer(
        """1. Смотреть анкеты.
2. Заполнить анкету заново.
3. Изменить фото/видео.
4. Изменить текст анкеты.""",
        reply_markup=kbr.my_profile,
    )
    await state.set_state(ProfileStates.action)


@router.message(ProfileStates.action, F.text == "4")
async def change_profile_text(message: Message, state: FSMContext):
    await message.answer(
        "Расскажи о себе, кого хочешь найти, чем предлагаешь заняться",
        reply_markup=kbr.back_profile,
    )
    await state.set_state(ProfileStates.change_text)


@router.message(ProfileStates.change_text)
async def changing_text(message: Message, state: FSMContext):
    await users.set_user_about(message.from_user.id, message.text)
    await state.clear()
    await my_profile(message, state)
