import re
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database.requests.users as users

from utils.resoulve_username import resolve_username_to_user_id

router = Router()

class Admin(StatesGroup):
    remove_admin = State()


@router.callback_query(F.data == 'remove_admin')
async def set_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите @юз админа для снятия')
    await state.set_state(Admin.remove_admin)


@router.message(Admin.remove_admin)
async def set_admin(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == 'назад':
        await message.answer('Отменено.')
        await state.clear()
    else:
        mention = re.search(r'@(\w+)', message.text)

        if mention:
            username = mention.group(1)
            remove_admin_id = await resolve_username_to_user_id(username)
            if remove_admin_id != message.from_user.id:
                user = await users.get_user(remove_admin_id)
                if user:
                    await users.set_user_role(remove_admin_id, 'user')
                    await message.answer(f'Вы успешно разжаловали админа @{username}')
                    await bot.send_message(chat_id=remove_admin_id, text='<b>Вас сняли с поста администратора</b>',
                                           parse_mode=ParseMode.HTML)
                else:
                    await message.answer('Пользователь не зарегистрирован в боте')
            else:
                await message.answer('Вы не можете снять себя с поста.')

        await state.clear()
