import shortuuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Api"]
)


@router.post("/create-short-link")
def create_short_link(link: str, db: Session = Depends(get_db)) -> str:
    record = db.query(models.LinkTable).filter_by(link=link).first()
    # print(link)
    if record:
        short_link = record.short_link
    else:
        short_link = shortuuid.uuid()[:8]

        # Additional check
        while db.query(models.LinkTable).filter_by(short_link=short_link).first():
            short_link = shortuuid.uuid()[:8]

        db_link = models.LinkTable(link=link, short_link=short_link)

        db.add(db_link)
        db.commit()
        db.refresh(db_link)
    return short_link
