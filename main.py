from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, SessionLocal, get_db
from pages.router import router as router_pages
from api.router import router as router_api
import models
import shortuuid

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Short URL"
)

app.include_router(router_pages)
app.include_router(router_api)


# def get_db():
#     db = SessionLocal()
#     try:
#         return db
#     finally:
#         db.close()


# class Link(BaseModel):
#     id: int
#     link: str
#     short_link: str


# @app.post("/create-short-link")
# def create_short_link(link: str, db: Session = Depends(get_db)) -> str:
#     record = db.query(models.LinkTable).filter_by(link=link).first()
#
#     if record:
#         short_link = record.short_link
#     else:
#         short_link = shortuuid.uuid()[:8]
#
#         db_link = models.LinkTable(link=link, short_link=short_link)
#
#         db.add(db_link)
#         db.commit()
#         db.refresh(db_link)
#     return short_link


@app.get("/{short_link}")
def redirect(short_link: str, db: Session = Depends(get_db)):
    record = db.query(models.LinkTable).filter_by(short_link=short_link).first()

    if record:
        record.total_clicks += 1
        db.commit()
        return RedirectResponse(url=record.link)
    else:
        raise HTTPException(status_code=404, detail="Short link not found")