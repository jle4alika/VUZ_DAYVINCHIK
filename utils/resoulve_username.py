from pyrogram import Client
from config import settings

async def resolve_username_to_user_id(username: str) -> int | None:
    async with Client(
                settings.SHORT_NAME,
                api_id=settings.API_ID,
                api_hash=settings.API_HASH,
                bot_token=settings.TOKEN,
                in_memory=False) as ubot:
        try:
            user = await ubot.get_users(username)
            return user.id
        except Exception as err:
            print(err)