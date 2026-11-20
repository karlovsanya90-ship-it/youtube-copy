from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.channel import Channel
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    # Проверяем, есть ли уже такой пользователь
    existing = await db.scalar(select(User).where(User.email == data.email))
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    # Создаем пользователя
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role="user"
    )
    db.add(user)
    await db.flush() # Получаем ID пользователя до коммита

    # Создаем канал для пользователя
    channel = Channel(
        owner_id=user.id,
        name=data.channel_name,
        description=f"Добро пожаловать на канал {data.channel_name}!"
    )
    db.add(channel)
    await db.commit()
    await db.refresh(user)

    return UserResponse(
        id=str(user.id),
        email=user.email,
        role=user.role,
        channel_name=data.channel_name
    )

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await db.scalar(select(User).where(User.email == data.email))

    # Если пользователя нет или пароль неверный
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    # Генерируем токен
    token = create_access_token(str(user.id), user.role)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
async def get_me(user: Annotated[User, Depends(get_current_user)], db: Annotated[AsyncSession, Depends(get_db)]):
    # Получаем канал пользователя для ответа
    channel = await db.scalar(select(Channel).where(Channel.owner_id == user.id))
    channel_name = channel.name if channel else "Без канала"

    return UserResponse(
        id=str(user.id),
        email=user.email,
        role=user.role,
        channel_name=channel_name
    )