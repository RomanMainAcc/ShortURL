from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from shorturl.core.database.database import get_async_session
from shorturl.core.models import models

router = APIRouter(
    prefix="",
    tags=["Redirect"]
)


@router.get("/{short_link}")
async def redirect(short_link: str, db: AsyncSession = Depends(get_async_session)):
    statement = select(models.LinkTable).where(and_(models.LinkTable.short_link == short_link))
    result = await db.execute(
        statement
    )
    record: models.LinkTable = result.scalar_one_or_none()
    if record:
        record.total_clicks += 1
        await db.commit()
        return RedirectResponse(url=record.link)
    else:
        raise HTTPException(status_code=404, detail="Short link not found")
