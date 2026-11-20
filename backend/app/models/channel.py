import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import BaseModel

class Channel(Base, BaseModel):
    __tablename__ = "channels"

    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String, default="")

    owner: Mapped["User"] = relationship(back_populates="channel")
    videos: Mapped[list["Video"]] = relationship(back_populates="channel")
    playlists: Mapped[list["Playlist"]] = relationship(back_populates="channel")