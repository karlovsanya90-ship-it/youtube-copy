from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

bearer = HTTPBearer(auto_error=False)


async def get_current_user_optional(
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
        db: Annotated[AsyncSession, Depends(get_db)],
) -> User | None:
    if credentials is None:
        return None
    try:
        payload = decode_token(credentials.credentials)
    except ValueError:
        return None
    if payload.get("type") != "access":
        return None
    user = await db.scalar(select(User).where(User.id == payload["sub"]))
    return user


async def get_current_user(
        user: Annotated[User | None, Depends(get_current_user_optional)],
) -> User:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


def require_role(*roles: str):
    async def _checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user

    return _checker