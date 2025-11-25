from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from database.requests.users import get_user

router = Router()


@router.message(Command('admin'))
async def admin(message: Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)

    if user.role == 'admin':
        await message.answer('Вы успешно вошли в админ панель',
                             # reply_markup=kb.admin
        )

