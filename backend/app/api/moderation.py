from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.deps import get_db, require_role
from app.models.user import User
from app.models.video import Video

router = APIRouter()

@router.patch("/videos/{video_id}/hide")
async def hide_video(
        video_id: UUID,
        user: Annotated[User, Depends(require_role("moderator", "admin"))],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    video = await db.scalar(select(Video).where(Video.id == video_id))
    if not video:
        raise HTTPException(status_code=404, detail="Видео не найдено")

    # Скрываем видео
    video.status = "hidden"
    await db.commit()
    return {"status": "hidden", "message": f"Видео {video.title} скрыто модератором"}

@router.patch("/videos/{video_id}/unhide")
async def unhide_video(
        video_id: UUID,
        user: Annotated[User, Depends(require_role("moderator", "admin"))],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    video = await db.scalar(select(Video).where(Video.id == video_id))
    if not video:
        raise HTTPException(status_code=404, detail="Видео не найдено")

    video.status = "ready"
    await db.commit()
    return {"status": "ready", "message": f"Видео {video.title} восстановлено"}