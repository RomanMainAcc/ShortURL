from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from shorturl.core.database.database import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String, nullable=False)

    links = relationship("LinkTable", back_populates="user")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
