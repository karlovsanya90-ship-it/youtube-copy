from fastapi import APIRouter
from app.api import auth, videos, comments, likes, search, moderation, subscriptions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(videos.router, prefix="/videos", tags=["videos"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(likes.router, prefix="/likes", tags=["likes"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(moderation.router, prefix="/moderation", tags=["moderation"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"]) # Добавили