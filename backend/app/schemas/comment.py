from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CommentCreateRequest(BaseModel):
    body: str

class CommentResponse(BaseModel):
    id: UUID
    body: str
    user_id: UUID
    author_name: str  # <-- Добавили имя автора
    created_at: datetime