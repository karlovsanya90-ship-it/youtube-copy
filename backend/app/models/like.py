import uuid
from sqlalchemy import ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Like(Base):
    __tablename__ = "likes"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    video_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"), primary_key=True)
    value: Mapped[int] = mapped_column(SmallInteger)  # 1 = лайк, -1 = дизлайк

    video: Mapped["Video"] = relationship(back_populates="likes")