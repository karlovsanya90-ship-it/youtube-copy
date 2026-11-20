from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.video import Video
from app.models.channel import Channel
from app.schemas.video import VideoResponse
from app.services.storage import storage

router = APIRouter()

@router.post("/upload", response_model=VideoResponse, status_code=201)
async def upload_video(
        title: Annotated[str, Form()],
        description: Annotated[str, Form()] = "",
        visibility: Annotated[str, Form()] = "public",
        file: UploadFile = File(...),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    channel = await db.scalar(select(Channel).where(Channel.owner_id == user.id))
    if not channel:
        raise HTTPException(status_code=400, detail="У вас нет канала")

    video = Video(
        channel_id=channel.id,
        title=title,
        description=description,
        visibility=visibility,
        status="processing"
    )
    db.add(video)
    await db.flush()

    try:
        filename = storage.save_video(str(video.id), file)
        video.storage_key = filename
        video.status = "ready"
        await db.commit()
        await db.refresh(video)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}")

    return video

@router.get("/", response_model=list[VideoResponse])
async def get_videos(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.scalars(
        select(Video).where(Video.visibility == "public", Video.status == "ready")
        .order_by(Video.created_at.desc())
    )
    return result.all()

from fastapi.responses import FileResponse
from uuid import UUID

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    video = await db.scalar(select(Video).where(Video.id == video_id))
    if not video:
        raise HTTPException(status_code=404, detail="Видео не найдено")
    return video

@router.get("/{video_id}/stream")
async def stream_video(video_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    video = await db.scalar(select(Video).where(Video.id == video_id))
    if not video or not video.storage_key:
        raise HTTPException(status_code=404, detail="Видео не найдено или не обработано")

    # Проверка прав (если видео приватное)
    if video.visibility == "private":
        # В реальном проекте тут будет проверка токена пользователя,
        # но для упрощения пока разрешаем всем (или можно добавить проверку)
        pass

    file_path = storage.get_video_path(video.storage_key)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл физически отсутствует на диске")

    return FileResponse(file_path, media_type="video/mp4", filename=video.storage_key)