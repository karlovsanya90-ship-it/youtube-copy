from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    secret_key: str = Field(..., min_length=32)
    access_token_ttl_min: int = 15
    refresh_token_ttl_days: int = 7
    cors_origins: str = "http://localhost:3000"

    postgres_user: str = "youtube"
    postgres_password: str = "youtube"
    postgres_db: str = "youtube"
    postgres_host: str = "db"
    postgres_port: int = 5432

    s3_endpoint: str = "http://minio:9000"
    s3_public_endpoint: str = "http://localhost:9000"
    s3_bucket: str = "videos"
    s3_region: str = "us-east-1"
    minio_root_user: str = "minioadmin"
    minio_root_password: str = "minioadmin"

    redis_url: str = "redis://redis:6379/0"

    max_upload_mb: int = 2048
    presign_ttl_sec: int = 900

    # --- Настройки для локального хранилища (вместо MinIO) ---
    storage_type: str = "local"
    local_storage_path: str = "C:/Users/user/Projects/youtube-copy/media"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()