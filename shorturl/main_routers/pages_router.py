from typing import Optional

from fastapi import APIRouter, Request, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from main import fastapi_users
from shorturl.auth.database import User
from shorturl.auth.manager import UserManager, get_user_manager
from shorturl.auth.schemas import UserCreate
from shorturl.core.database.database import get_async_session
from shorturl.core.models import models

router = APIRouter(
    prefix="",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="shorturl/core/templates")


@router.get("/base", response_class=HTMLResponse)
def get_base_page(request: Request, user: Optional[User] = Depends(fastapi_users.current_user(optional=True))):
    return templates.TemplateResponse("base.html", {"request": request, "user": user})


@router.get("/", response_class=HTMLResponse)
def get_shortener_page(
    request: Request,
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
):
    return templates.TemplateResponse("shortener.html", {"request": request, "user": user})


@router.get("/records/{short_link}", response_class=HTMLResponse)
async def get_report_page(
    short_link: str,
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
):
    # record = db.query(models.LinkTable).filter_by(short_link=short_link).first()
    result = await db.execute(
        select(models.LinkTable).where(and_(models.LinkTable.short_link == short_link))
    )
    record: models.LinkTable = result.scalar_one_or_none()
    # mm = result.scalar()
    if not record:
        raise HTTPException(status_code=404, detail="Short link not found")
    return templates.TemplateResponse("report.html", {"request": request, "record": record, "user": user})


@router.get("/records", response_class=HTMLResponse)
async def get_records_page(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True)),
):
    # records = db.query(models.LinkTable).all()
    result = await db.execute(
        select(models.LinkTable)
    )
    records: list[models.LinkTable] = result.scalars().all()  # type: Ignore

    return templates.TemplateResponse("records.html", {"request": request, "records": records, "user": user})


@router.get("/signup", response_class=HTMLResponse)
async def registration_form(
    request: Request,
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True)),
):
    return templates.TemplateResponse("signup.html", {"request": request, "user": user})


@router.post("/signup")
async def signup_post(
    request: Request,
    user_manager: UserManager = Depends(get_user_manager),
    email: EmailStr = Form(),
    password: str = Form(),
    username: str = Form(),
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
):
    credentials = UserCreate(email=email, password=password, username=username)
    try:

        await user_manager.create(credentials)

        return RedirectResponse(status_code=status.HTTP_303_SEE_OTHER, url="/login")

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid credentials")


@router.get("/login", response_class=HTMLResponse)
async def login_form(
    request: Request,
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})


@router.get("/user/homepage", response_class=HTMLResponse)
async def homepage(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(fastapi_users.current_user(active=True))
):
    result = await db.execute(
        select(models.LinkTable).where(and_(models.LinkTable.user_id == user.id))
    )
    records: list[models.LinkTable] = result.scalars().all()  # type: Ignore
    # mm = result.scalar()
    if not records:
        raise HTTPException(status_code=404, detail="Short link not found")

    return templates.TemplateResponse("homepage.html", {"request": request, "user": user, "records": records})

# @router.post("/login", response_class=HTMLResponse)
# async def login_post(
#     request: Request,
#     user_manager: UserManager = Depends(get_user_manager),
#     email: EmailStr = Form(),
#     password: str = Form(),
# ):
#     form_data = OAuth2PasswordRequestForm(username=email, password=password)
#     try:
#
#         user = await user_manager.authenticate(form_data)
#
#         jwt_content = {"sub": str(user.id)}
#         jwt_token = encode(jwt_content, SECRET, algorithm="HS256")
#
#         response = templates.TemplateResponse("shortener.html", {"request": request})
#         response.set_cookie(key="access_token", value=jwt_token, httponly=True, secure=False)
#         return response
#
#     except Exception:
#         raise HTTPException(status_code=400, detail="Invalid credentials")

# @router.post(
#         "/login",
#         name=f"auth:{backend.name}.login",
#         responses=login_responses,
#     )
#     async def login(
#         request: Request,
#         user_manager: UserManager = Depends(get_user_manager),
#         email: EmailStr = Form(),
#         password: str = Form(),
#         strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
#     ):
#         credentials = UserCreate(email=email, password=password)
#         user = await user_manager.authenticate(credentials)
#
#         if user is None or not user.is_active:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
#             )
#         if requires_verification and not user.is_verified:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
#             )
#         response = await backend.login(strategy, user)
#         await user_manager.on_after_login(user, request, response)
#         return response


# @router.post(
#         "/login",
#         name=f"auth:{backend.name}.login",
#         responses=login_responses,
#     )
#     async def login(
#         request: Request,
#         credentials: OAuth2PasswordRequestForm = Depends(),
#         user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
#         strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
#     ):
#         user = await user_manager.authenticate(credentials)
#
#         if user is None or not user.is_active:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
#             )
#         if requires_verification and not user.is_verified:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
#             )
#         response = await backend.login(strategy, user)
#         await user_manager.on_after_login(user, request, response)
#         return response
