from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ContentType, ReplyKeyboardRemove
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import database.requests.users as users

import keyboards.reply_keyboards.main as kbr
from utils.coordinates import resolve_city
from utils.user_profile import save_file, user_profile

router = Router()


class NewUserProfile(StatesGroup):
    age = State()
    gender = State()
    interest = State()
    name = State()
    city = State()
    phone_number = State()
    about = State()
    media = State()
    media_count = State()

    confirm_profile = State()


@router.message(F.text == "👌 Ok")
async def okay(message: Message, state: FSMContext):
    await message.answer("Сколько тебе лет?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewUserProfile.age)


@router.message(NewUserProfile.age)
async def reg_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введи возраст числом.")

    age = int(message.text)
    if not 10 <= age <= 99:
        return await message.answer("Возраст должен быть от 10 до 99.")

    await state.update_data(age=age)
    await users.set_user_age(message.from_user.id, age)

    await state.set_state(NewUserProfile.gender)
    await message.answer("Теперь определимся с полом", reply_markup=kbr.my_gender)


@router.message(NewUserProfile.gender, F.text.in_({"Я парень", "Я девушка"}))
async def reg_gender(message: Message, state: FSMContext):
    gender_map = {"Я парень": "male", "Я девушка": "female"}
    gender = gender_map[message.text]

    await state.update_data(gender=gender)
    await users.set_user_gender(message.from_user.id, gender)

    await state.set_state(NewUserProfile.interest)
    await message.answer("Кто тебе интересен?", reply_markup=kbr.interest_kb)


@router.message(NewUserProfile.interest, F.text.in_({"Девушки", "Парни", "Всё равно"}))
async def reg_interest(message: Message, state: FSMContext):
    interest_map = {"Девушки": "female", "Парни": "male", "Всё равно": "any"}
    interest = interest_map[message.text]

    await state.update_data(interest=interest)
    await users.set_user_looking_for(message.from_user.id, interest)

    await state.set_state(NewUserProfile.name)
    await message.answer("Как мне тебя называть?", reply_markup=ReplyKeyboardRemove())


@router.message(NewUserProfile.name)
async def reg_name(message: Message, state: FSMContext):
    name = message.text.strip()

    await state.update_data(name=name)
    await users.set_user_name(message.from_user.id, name)

    await state.set_state(NewUserProfile.city)
    await message.answer("Из какого ты института?")


@router.message(NewUserProfile.city, F.text)
async def reg_city_text(message: Message, state: FSMContext):
    city_name = message.text.strip()

    await state.update_data(city=city_name)
    await users.set_user_city(message.from_user.id, city_name)

    await state.set_state(NewUserProfile.about)
    await message.answer("Расскажи о себе", reply_markup=kbr.skip_description_kb)


@router.message(NewUserProfile.about)
async def reg_about(message: Message, state: FSMContext):
    about = message.text.strip()

    if message.text != "Пропустить":
        await state.update_data(about=about)
        await users.set_user_about(message.from_user.id, about)

    # Теперь начинаем добавление медиа после about
    await state.update_data(media_list=[], current_media_count=0)
    await state.set_state(NewUserProfile.media)
    await message.answer(
        "Теперь пришли фото или запиши видео 👍 (до 15 сек), его будут видеть другие пользователи"
    )


@router.message(NewUserProfile.media, F.photo | F.video)
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


@router.message(NewUserProfile.media, F.text == "Это всё, сохранить фото")
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
    await message.answer(
        "Так выглядит твоя анкета:",
    )
    media = await user_profile(message.from_user.id)
    await message.answer_media_group(media)
    await message.answer("Все верно?", reply_markup=kbr.confirm_profile_kb)
    await state.set_state(NewUserProfile.confirm_profile)


@router.message(NewUserProfile.confirm_profile)
async def confirm_profile(message: Message, state: FSMContext):
    await state.clear()
    if message.text == "Да":
        from handlers.user_handlers.search import search

        await search(message, state)
        return

    await message.answer("Сколько тебе лет?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(NewUserProfile.age)


@router.message(NewUserProfile.media)
async def invalid_media(message: Message):
    await message.answer(
        "Пожалуйста, отправь фото или видео, либо команду 'Это всё, сохранить фото', чтобы завершить."
    )


@router.message(NewUserProfile.gender)
async def invalid_gender(message: Message):
    await message.answer("Пожалуйста, выбери пол кнопкой.")


@router.message(NewUserProfile.interest)
async def invalid_interest(message: Message):
    await message.answer("Пожалуйста, выбери интерес кнопкой.")


@router.message(NewUserProfile.city)
async def invalid_city(message: Message):
    await message.answer("Пожалуйста, введи город или отправь геолокацию.")


@router.message(NewUserProfile.phone_number)
async def invalid_phone(message: Message):
    await message.answer("Пожалуйста, отправь номер через кнопку.")


@router.message(NewUserProfile.name)
async def invalid_name(message: Message):
    await message.answer("Пожалуйста, введи имя или ник.")
