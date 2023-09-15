from sqlalchemy import select

from shorturl.core.models import models
from tests.conftest import client


async def test_register(get_async_session, ac):
    db_link = models.LinkTable(link="sadasdsad", short_link="short dsadasd", user_id= None)

    get_async_session.add(db_link)
    await get_async_session.commit()
    await get_async_session.refresh(db_link)

    result = await get_async_session.execute(
        select(models.LinkTable)
    )
    records: list[models.LinkTable] = result.scalars().all()  # type: Ignore

    response = await ac.post("/auth/register", json={
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "K1jnqfXtGvxbQa4uaQJp3Lc5X2Q2UGtJaKm5uU93dj"
    }
    )
    assert response.status_code == 201


