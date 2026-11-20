import asyncio
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.user import User
from app.models.channel import Channel
from app.core.security import hash_password

async def main():
    async with SessionLocal() as db:
        # Проверяем, есть ли уже админ
        existing = await db.scalar(select(User).where(User.email == "admin@test.ru"))
        if existing:
            print("Тестовые пользователи уже созданы!")
            return

        users_data = [
            {"email": "admin@test.ru", "password": "password123", "role": "admin", "channel": "Админ Канал"},
            {"email": "mod@test.ru", "password": "password123", "role": "moderator", "channel": "Модератор Канал"},
            {"email": "user@test.ru", "password": "password123", "role": "user", "channel": "Юзер Канал"},
        ]

        for u in users_data:
            user = User(
                email=u["email"],
                password_hash=hash_password(u["password"]),
                role=u["role"]
            )
            db.add(user)
            await db.flush()

            channel = Channel(
                owner_id=user.id,
                name=u["channel"],
                description=f"Это канал пользователя {u['email']}"
            )
            db.add(channel)

        await db.commit()
        print("Успешно созданы тестовые пользователи!")

if __name__ == "__main__":
    asyncio.run(main())