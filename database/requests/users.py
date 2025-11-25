from sqlalchemy import func, select, update, delete, or_

from database.models import User, Dislike, Like, Message, Match
from database.db import async_session


async def create_dislike(tg_id: int, to_user_tg_id: int):
    async with async_session() as session:
        new = Dislike(tg_id=tg_id, to_user_tg_id=to_user_tg_id)
        session.add(new)
        await session.commit()


async def create_like(tg_id: int, to_user_tg_id: int):
    async with async_session() as session:
        new = Like(tg_id=tg_id, to_user_tg_id=to_user_tg_id)
        session.add(new)
        await session.commit()


async def create_match(tg_id: int, to_user_tg_id: int):
    async with async_session() as session:
        new = Match(tg_id=tg_id, to_user_tg_id=to_user_tg_id)
        session.add(new)
        await session.commit()


async def create_message(
    tg_id: int, to_user_tg_id: int, text: str = "", file: str = ""
):
    async with async_session() as session:
        new = Message(tg_id=tg_id, to_user_tg_id=to_user_tg_id, text=text, file=file)
        session.add(new)
        await session.commit()


async def get_or_create_user(tg_id: int, username: str) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            new_user = User(tg_id=tg_id, username=username)
            session.add(new_user)
            await session.commit()

        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def update_user_last_activity(tg_id: int):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(last_activity=func.now())
        )
        await session.commit()


async def get_user(tg_id: int) -> User | None:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def set_user_name(tg_id: int, name: str):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(name=name))
        await session.commit()


async def set_user_age(tg_id: int, age: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(age=age))
        await session.commit()


async def set_user_role(tg_id: int, role: str):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(role=role))
        await session.commit()


async def set_user_phone_number(tg_id: int, phone_number: str):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(phone_number=phone_number)
        )
        await session.commit()


async def set_user_about(tg_id: int, about: str):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(about=about)
        )
        await session.commit()


async def set_user_gender(tg_id: int, gender: str):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(gender=gender)
        )
        await session.commit()


async def set_user_looking_for(tg_id: int, looking_for: str):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(looking_for=looking_for)
        )
        await session.commit()


async def set_user_city(tg_id: int, city: str):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(city_name=city)
        )
        await session.commit()


async def set_user_coordinates(tg_id: int, latitude: float, longitude: float):
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(latitude=latitude, longitude=longitude)
        )
        await session.commit()


async def set_user_files(tg_id: int, files: str):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(files=files)
        )
        await session.commit()


async def get_users() -> list[User]:
    async with async_session() as session:
        query = await session.scalars(select(User))
        result = query.fetchall()

        return result


async def get_user_likes(tg_id: int) -> list[int]:
    async with async_session() as session:
        query1 = await session.scalars(
            select(Like.to_user_tg_id).where(Like.tg_id == tg_id)
        )
        result1 = query1.fetchall()

        query2 = await session.scalars(
            select(Like.tg_id).where(Like.to_user_tg_id == tg_id)
        )
        result2 = query2.fetchall()

        result = result1 + result2
        return result


async def get_user_unchecked_likes(tg_id: int) -> list[int]:
    async with async_session() as session:
        query = await session.scalars(
            select(Like.tg_id).where(Like.to_user_tg_id == tg_id, Like.checked == False)
        )
        result = query.fetchall()
        return result


async def like_checked(tg_id: int, to_user_tg_id: int):
    async with async_session() as session:
        await session.execute(
            update(Like)
            .where(Like.tg_id == tg_id, Like.to_user_tg_id == to_user_tg_id)
            .values(checked=True)
        )
        await session.commit()


async def get_user_matches(tg_id: int) -> list[int]:
    async with async_session() as session:
        query1 = await session.scalars(
            select(Match.to_user_tg_id).where(Match.tg_id == tg_id)
        )
        result1 = query1.fetchall()

        query2 = await session.scalars(
            select(Match.tg_id).where(Match.to_user_tg_id == tg_id)
        )
        result2 = query2.fetchall()

        result = result1 + result2
        return result


async def get_user_dislikes(tg_id: int) -> list[int]:
    async with async_session() as session:
        query1 = await session.scalars(
            select(Dislike.to_user_tg_id).where(Dislike.tg_id == tg_id)
        )
        result1 = query1.fetchall()

        query2 = await session.scalars(
            select(Dislike.tg_id).where(Dislike.to_user_tg_id == tg_id)
        )
        result2 = query2.fetchall()

        result = result1 + result2
        return result


async def search(tg_id: int):
    async with async_session() as session:
        user_looking_for = await session.scalar(
            select(User.looking_for).where(User.tg_id == tg_id)
        )

        if user_looking_for == "any":
            users = await session.scalars(
                select(User.tg_id).where(User.tg_id != tg_id, User.files != "")
            )
        else:
            users = await session.scalars(
                select(User.tg_id).where(
                    User.tg_id != tg_id,
                    User.files != "",
                    User.gender == user_looking_for,
                )
            )

        user_likes = await get_user_likes(tg_id)
        user_dislikes = await get_user_dislikes(tg_id)
        user_matches = await get_user_matches(tg_id)

        return [
            user
            for user in users
            if user not in user_likes
            and user not in user_dislikes
            and user not in user_matches
        ]


async def message_to_user(tg_id: int, to_user_tg_id: int) -> None | Message:
    async with async_session() as session:
        return await session.scalar(
            select(Message).where(
                Message.tg_id == tg_id, Message.to_user_tg_id == to_user_tg_id
            )
        )
