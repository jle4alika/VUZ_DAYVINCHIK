import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.db import async_main
from config import settings
from middlewares.user_last_activity import LastActivityMiddleware
from handlers.user_handlers import (
    start,
    search,
    registration,
    main_menu,
    my_profile,
    check_likes,
)
from handlers.admin_handlers.admin_access import (
    admin_menu,
    create_admin,
    remove_admin,
)

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():
    await async_main()
    bot = Bot(token=settings.TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    logging.basicConfig(
        level=logging.INFO,
        filename="logs.txt",
        format="%(asctime)s - [%(levelname)s] - [%(threadName)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )

    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    scheduler = AsyncIOScheduler()

    # scheduler.add_job(
    #     check_referrals, trigger="interval", minutes=1, kwargs={"bot": Bot}
    # )
    # scheduler.add_job(check_fires, trigger="interval", hours=12, kwargs={"bot": Bot})
    # scheduler.add_job(
    #     create_new_week_statistic, trigger="cron", hour=0, kwargs={"bot": Bot}
    # )
    # scheduler.add_job(check_likes, trigger="cron", day=1)

    scheduler.start()

    logger.info("Starting BOT")

    dp.include_router(admin_menu.router)
    dp.include_router(create_admin.router)
    dp.include_router(remove_admin.router)

    dp.include_router(start.router)
    dp.include_router(registration.router)
    dp.include_router(main_menu.router)
    dp.include_router(my_profile.router)
    # dp.include_router(check_likes.router)
    dp.include_router(search.router)

    dp.message.middleware(LastActivityMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    commands = [BotCommand(command="start", description="Перезапустить бота")]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
