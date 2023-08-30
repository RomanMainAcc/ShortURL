import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi.responses import RedirectResponse
from fastapi import status, Response
from fastapi_users.authentication import JWTStrategy
from config import SECRET
from shorturl.auth.database import User
from shorturl.auth.manager import get_user_manager


class CookieTransportRedirect(CookieTransport):
    async def get_login_response(self, token: str) -> Response:
        response = RedirectResponse(status_code=status.HTTP_303_SEE_OTHER, url="/")

        return self._set_login_cookie(response, token)


cookie_transport = CookieTransportRedirect(cookie_max_age=3600)


SECRET = SECRET


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
