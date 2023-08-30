import uuid
from pydantic import Field

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(..., pattern="^[a-zA-Z0-9_]+$")


class UserUpdate(schemas.BaseUserUpdate):
    pass
