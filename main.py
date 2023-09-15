from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import STATIC_DIR
from shorturl.auth.auth import auth_backend, fastapi_users
from shorturl.auth.schemas import UserRead, UserCreate
from shorturl.main_routers.pages_router import router as router_pages
from shorturl.main_routers.redirect_router import router as redirect_router
from shorturl.rest_api_routers.link_routes import router as router_api

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Short URL"
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(router_pages)
app.include_router(router_api)
app.include_router(redirect_router)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
