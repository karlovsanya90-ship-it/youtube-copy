from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "youtube_copy",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.task_default_queue = "default"
celery_app.conf.broker_connection_retry_on_startup = True