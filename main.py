from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import engine, SessionLocal, get_db
from pages.router import router as router_pages
from api.router import router as router_api
import models
from ShortURL_app.main_routers.redirect_router import router as redirect_router

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Short URL"
)

app.include_router(router_pages)
app.include_router(router_api)
app.include_router(redirect_router)
