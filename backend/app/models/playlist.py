import uuid
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import BaseModel

class Playlist(Base, BaseModel):
    __tablename__ = "playlists"

    channel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("channels.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))

    channel: Mapped["Channel"] = relationship(back_populates="playlists")
    items: Mapped[list["PlaylistItem"]] = relationship(back_populates="playlist")

class PlaylistItem(Base):
    __tablename__ = "playlist_items"

    playlist_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("playlists.id", ondelete="CASCADE"), primary_key=True)
    video_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), primary_key=True)
    position: Mapped[int] = mapped_column(Integer, default=0)

    playlist: Mapped["Playlist"] = relationship(back_populates="items")