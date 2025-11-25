import re
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.resoulve_username import resolve_username_to_user_id

import database.requests.users as users


router = Router()

class Admin(StatesGroup):
    new_admin = State()


@router.callback_query(F.data == 'set_admin')
async def set_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите @юз нового админа')
    await state.set_state(Admin.new_admin)


@router.message(Admin.new_admin)
async def set_admin(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == 'назад':
        await message.answer('Отменено.')
        await state.clear()
    else:
        mention = re.search(r'@(\w+)', message.text)
        if mention:
            username = mention.group(1)

            new_admin_id = await resolve_username_to_user_id(username)
            if new_admin_id != message.from_user.id:
                user = await users.get_user(new_admin_id)
                if user:
                    await users.set_user_role(new_admin_id, 'admin')
                    await message.answer(f'Вы успешно назначили админа @{username}')
                    await bot.send_message(chat_id=new_admin_id, text='<b>Вас назначили администратором!</b>',
                                           parse_mode=ParseMode.HTML)
                else:
                    await message.answer('Пользователь не зарегистрирован в боте')
            else:
                await message.answer('Вы не можете назначить себя на пост администратора.')
        await state.clear()

