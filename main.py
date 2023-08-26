from fastapi import FastAPI

from ShortURL_app.main_routers.pages_router import router as router_pages
from ShortURL_app.rest_api_routers.router import router as router_api
from ShortURL_app.main_routers.redirect_router import router as redirect_router

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Short URL"
)

app.include_router(router_pages)
app.include_router(router_api)
app.include_router(redirect_router)
