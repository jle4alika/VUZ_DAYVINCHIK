import database.requests.users as users


async def check_likes():
    all_users = await users.get_users()

    for user in users:
        likes = await users.unchecked_likes(user)
