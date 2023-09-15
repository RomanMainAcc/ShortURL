import uuid

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(..., pattern="^[a-zA-Z0-9_]+$")


class UserUpdate(schemas.BaseUserUpdate):
    pass
