import uuid
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import BaseModel

class Video(Base, BaseModel):
    __tablename__ = "videos"

    channel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("channels.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(String, default="")
    status: Mapped[str] = mapped_column(String(20), default="uploading")
    # uploading, processing, ready, failed, hidden
    visibility: Mapped[str] = mapped_column(String(20), default="public")
    # public, private, unlisted
    storage_key: Mapped[str | None] = mapped_column(String(255))
    thumbnail_key: Mapped[str | None] = mapped_column(String(255))
    duration_sec: Mapped[int | None] = mapped_column(Integer)

    channel: Mapped["Channel"] = relationship(back_populates="videos")
    comments: Mapped[list["Comment"]] = relationship(back_populates="video")
    likes: Mapped[list["Like"]] = relationship(back_populates="video")