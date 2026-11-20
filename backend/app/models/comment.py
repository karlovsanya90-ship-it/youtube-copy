import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import BaseModel

class Comment(Base, BaseModel):
    __tablename__ = "comments"

    video_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    parent_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("comments.id", ondelete="CASCADE"))
    body: Mapped[str] = mapped_column(String)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    video: Mapped["Video"] = relationship(back_populates="comments")