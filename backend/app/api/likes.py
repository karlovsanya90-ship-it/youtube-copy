from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.like import Like
from app.models.video import Video

router = APIRouter()

@router.post("/{video_id}/like", status_code=200)
async def like_video(
        video_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    video = await db.scalar(select(Video).where(Video.id == video_id))
    if not video:
        raise HTTPException(status_code=404, detail="Видео не найдено")

    # Проверяем, ставил ли уже лайк
    existing_like = await db.scalar(
        select(Like).where(Like.video_id == video_id, Like.user_id == user.id)
    )

    if existing_like:
        if existing_like.value == 1:
            # Если лайк уже есть — убираем его (дизлайк)
            await db.delete(existing_like)
            await db.commit()
            return {"status": "unliked"}
        else:
            # Если был дизлайк, меняем на лайк
            existing_like.value = 1
            await db.commit()
            return {"status": "liked"}
    else:
        # Ставим новый лайк
        new_like = Like(video_id=video_id, user_id=user.id, value=1)
        db.add(new_like)
        await db.commit()
        return {"status": "liked"}

@router.get("/{video_id}/likes")
async def get_likes(video_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    count = await db.scalar(
        select(func.count(Like.user_id)).where(Like.video_id == video_id, Like.value == 1)
    )
    return {"likes_count": count or 0}