from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.deps import get_db
from app.models.video import Video
from app.schemas.video import VideoResponse

router = APIRouter()

@router.get("/", response_model=list[VideoResponse])
async def search_videos(
        q: str,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    # Простой поиск по названию (ILIKE - нечувствителен к регистру)
    result = await db.scalars(
        select(Video)
        .where(
            Video.title.ilike(f"%{q}%"),
            Video.visibility == "public",
            Video.status == "ready"
        )
        .order_by(Video.created_at.desc())
    )
    return result.all()