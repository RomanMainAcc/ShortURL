from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import get_db

router = APIRouter(
    prefix="",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/")
def get_shortener_page(request: Request):
    return templates.TemplateResponse("shortener.html", {"request": request})


@router.get("/records/{short_link}")
def get_report_page(short_link: str, request: Request, db: Session = Depends(get_db)):
    record = db.query(models.LinkTable).filter_by(short_link=short_link).first()
    if not record:
        raise HTTPException(status_code=404, detail="Short link not found")
    return templates.TemplateResponse("report.html", {"request": request, "record": record})


@router.get("/records")
def get_records_page(request: Request, db: Session = Depends(get_db)):
    records = db.query(models.LinkTable).all()
    return templates.TemplateResponse("records.html", {"request": request, "records": records})
