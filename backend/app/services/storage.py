import shutil
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings

class LocalStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.videos_path = self.base_path / "videos"
        self.videos_path.mkdir(parents=True, exist_ok=True)

    def save_video(self, video_id: str, file: UploadFile) -> str:
        file_extension = Path(file.filename).suffix or ".mp4"
        filename = f"{video_id}{file_extension}"
        file_path = self.videos_path / filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return filename

    def get_video_path(self, filename: str) -> Path:
        return self.videos_path / filename

storage = LocalStorage(settings.local_storage_path)