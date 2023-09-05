from typing import Optional

import shortuuid
from fastapi import APIRouter, Depends
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from shorturl.auth.auth import fastapi_users
from shorturl.auth.database import User
from shorturl.core.database.database import get_async_session
from shorturl.core.models import models
from shorturl.core.schemas.link_schemas import Link

router = APIRouter(
    prefix="/api",
    tags=["Api"]
)


@router.post("/create-short-link", response_model=str)
async def create_short_link(
    link: Link,
    db: AsyncSession = Depends(get_async_session),
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True)),
):
    link_str = str(link.link)
    result = await db.execute(
        select(models.LinkTable).where(and_(models.LinkTable.link == link_str))
    )
    record = result.scalar_one_or_none()

    if record:
        short_link = record.short_link
    else:
        short_link = shortuuid.uuid()[:8]

        # Additional check
        # while db.query(models.LinkTable).filter_by(short_link=short_link).first():
        #     short_link = shortuuid.uuid()[:8]

        db_link = models.LinkTable(link=link_str, short_link=short_link, user_id=user.id if user else None)

        db.add(db_link)
        await db.commit()
        await db.refresh(db_link)
    return short_link
