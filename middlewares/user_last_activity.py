from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from database.requests.users import update_user_last_activity

class LastActivityMiddleware(BaseMiddleware):
    """
    Middleware for last user activity with bot
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Определяем tg_id из события (Message или CallbackQuery)
        tg_id = None
        if isinstance(event, Message):
            tg_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            tg_id = event.from_user.id

        if tg_id:
            await update_user_last_activity(tg_id)

        return await handler(event, data)