from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class VideoCreateRequest(BaseModel):
    title: str
    description: str = ""
    visibility: str = "public"

class VideoResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    visibility: str
    channel_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True