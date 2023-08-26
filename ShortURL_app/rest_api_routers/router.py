import shortuuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ShortURL_app.core.models import models
from ShortURL_app.core.schemas.link_schemas import Link
from ShortURL_app.core.database.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Api"]
)


@router.post("/create-short-link", response_model=str)
def create_short_link(link: Link, db: Session = Depends(get_db)):
    link_str = str(link.link)
    record = db.query(models.LinkTable).filter_by(link=link_str).first()
    if record:
        short_link = record.short_link
    else:
        short_link = shortuuid.uuid()[:8]

        # Additional check
        while db.query(models.LinkTable).filter_by(short_link=short_link).first():
            short_link = shortuuid.uuid()[:8]

        db_link = models.LinkTable(link=link_str, short_link=short_link)

        db.add(db_link)
        db.commit()
        db.refresh(db_link)
    return short_link
