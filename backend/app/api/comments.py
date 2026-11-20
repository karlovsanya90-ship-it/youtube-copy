from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.video import Video
from app.models.comment import Comment
from app.models.channel import Channel
from app.schemas.comment import CommentCreateRequest, CommentResponse

router = APIRouter()

@router.get("/video/{video_id}", response_model=list[CommentResponse])
async def get_video_comments(video_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    # Делаем запрос с JOIN, чтобы сразу получить имя канала пользователя
    stmt = (
        select(Comment, Channel.name)
        .join(User, Comment.user_id == User.id)
        .join(Channel, Channel.owner_id == User.id)
        .where(Comment.video_id == video_id, Comment.deleted_at == None)
        .order_by(Comment.created_at.desc())
    )
    result = await db.execute(stmt)

    comments = []
    for comment, author_name in result:
        comments.append({
            "id": comment.id,
            "body": comment.body,
            "user_id": comment.user_id,
            "author_name": author_name,
            "created_at": comment.created_at
        })
    return comments

@router.post("/video/{video_id}", response_model=CommentResponse, status_code=201)
async def create_comment(
        video_id: UUID,
        data: CommentCreateRequest,
        user: Annotated[User, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_db)]
):
    video = await db.scalar(select(Video).where(Video.id == video_id))
    if not video:
        raise HTTPException(status_code=404, detail="Видео не найдено")

    comment = Comment(
        video_id=video_id,
        user_id=user.id,
        body=data.body
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)

    # Получаем имя канала для ответа
    channel = await db.scalar(select(Channel).where(Channel.owner_id == user.id))
    author_name = channel.name if channel else "Пользователь"

    return {
        "id": comment.id,
        "body": comment.body,
        "user_id": comment.user_id,
        "author_name": author_name,
        "created_at": comment.created_at
    }