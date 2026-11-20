from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_db, get_current_user, get_current_user_optional
from app.models.user import User
from app.models.channel import Channel
from app.models.subscription import Subscription

router = APIRouter()

@router.post("/{channel_id}")
async def subscribe(
        channel_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    channel = await db.scalar(select(Channel).where(Channel.id == channel_id))
    if not channel:
        raise HTTPException(status_code=404, detail="Канал не найден")

    if channel.owner_id == user.id:
        raise HTTPException(status_code=400, detail="Нельзя подписаться на свой канал")

    existing = await db.scalar(
        select(Subscription).where(
            Subscription.user_id == user.id,
            Subscription.channel_id == channel_id
        )
    )

    if existing:
        await db.delete(existing)
        await db.commit()
        return {"status": "unsubscribed"}
    else:
        sub = Subscription(user_id=user.id, channel_id=channel_id)
        db.add(sub)
        await db.commit()
        return {"status": "subscribed"}

@router.get("/{channel_id}/status")
async def get_subscription_status(
        channel_id: UUID,
        user: Annotated[User | None, Depends(get_current_user_optional)], # Теперь пользователь не обязателен
        db: Annotated[AsyncSession, Depends(get_db)]
):
    # Если пользователь не авторизован, он точно не подписан
    if not user:
        return {"is_subscribed": False}

    existing = await db.scalar(
        select(Subscription).where(
            Subscription.user_id == user.id,
            Subscription.channel_id == channel_id
        )
    )
    return {"is_subscribed": existing is not None}