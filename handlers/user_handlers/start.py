from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import database.requests.users as users

import keyboards.reply_keyboards.main as kbr
from utils.user_profile import user_profile

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    if not message.from_user.username:
        await message.answer("Установите юзернейм и возвращайтесь к нам!")
        return

    user = await users.get_user(message.from_user.id)
    print(user.__dict__)
    if not user:
        await users.get_or_create_user(message.from_user.id, message.from_user.username)
        await message.answer(
            """Я помогу найти тебе пару или просто друзей 👫""",
            reply_markup=kbr.start,
            parse_mode=ParseMode.HTML,
        )
    else:
        if (
            not user.age
            or not user.name
            or not user.phone_number
            or not user.gender
            or not user.looking_for
            or (not user.city_name or user.latitude and user.longitude)
            or not user.files
        ):
            await message.answer(
                """Я помогу найти тебе пару или просто друзей 👫""",
                reply_markup=kbr.start,
                parse_mode=ParseMode.HTML,
            )
            return

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


@router.message(F.text == "👌 давай начнем")
async def lets_go(message: Message):
    from aiogram.types.link_preview_options import LinkPreviewOptions

    await message.answer(
        """❗️ Помните, что в интернете люди могут выдавать себя за других.

Бот не запрашивает личные данные и не идентифицирует пользователей по каким-либо документам.

Продолжая, вы принимаете <a href="http://agreement.leomatchbot.com/">пользовательское соглашение</a> и <a href="http://privacy.leomatchbot.com/">политику конфиденциальности</a>.""",
        parse_mode=ParseMode.HTML,
        reply_markup=kbr.okay,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
