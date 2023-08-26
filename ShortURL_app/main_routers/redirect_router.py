from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ShortURL_app.core.models import models
from ShortURL_app.core.database.database import get_db

router = APIRouter(
    prefix="",
    tags=["Redirect"]
)


@router.get("/{short_link}")
def redirect(short_link: str, db: Session = Depends(get_db)):
    record = db.query(models.LinkTable).filter_by(short_link=short_link).first()

    if record:
        record.total_clicks += 1
        db.commit()
        return RedirectResponse(url=record.link)
    else:
        raise HTTPException(status_code=404, detail="Short link not found")