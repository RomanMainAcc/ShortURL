from typing import Optional

from jwt import encode
from fastapi import APIRouter, Request, Depends, HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi_users import jwt
from fastapi_users.authentication import CookieTransport, Strategy
from pydantic import EmailStr
from sqlalchemy.orm import Session

from config import SECRET
from main import fastapi_users
from shorturl.auth.database import User
from shorturl.auth.schemas import UserCreate
from shorturl.auth.manager import UserManager, get_user_manager
from shorturl.core.models import models
from shorturl.core.database.database import get_db


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
def get_report_page(
    short_link: str,
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True))
):
    record = db.query(models.LinkTable).filter_by(short_link=short_link).first()
    if not record:
        raise HTTPException(status_code=404, detail="Short link not found")
    return templates.TemplateResponse("report.html", {"request": request, "record": record, "user": user})


@router.get("/records", response_class=HTMLResponse)
def get_records_page(
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(fastapi_users.current_user(optional=True)),
):
    records = db.query(models.LinkTable).all()
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
def homepage(request: Request, user: User = Depends(fastapi_users.current_user(active=True))):
    return templates.TemplateResponse("homepage.html", {"request": request, "user": user})

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
