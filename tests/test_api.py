import pytest
from http import HTTPStatus
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src import Hero


@pytest.mark.asyncio
async def test_hero_post(async_client: AsyncClient, db_session: AsyncSession) -> None:
    response = await async_client.post("/hero/", params={"name": "batman"})

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    for hero in data:
        assert "batman" in hero["name"].lower()

    first_batman = data[0]
    batman = await db_session.get(Hero, 1)
    assert batman.name == first_batman["name"]


@pytest.mark.asyncio
async def test_hero_post_not_found(async_client: AsyncClient, db_session: AsyncSession) -> None:
    response = await async_client.post("/hero/", params={"name": "test_hero"})

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_hero_get(async_client: AsyncClient, db_session: AsyncSession) -> None:
    await async_client.post("/hero/", params={"name": "batman"})
    response = await async_client.get("/hero/", params={"name": "Batman"})

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_hero_get_with_filters(async_client: AsyncClient, db_session: AsyncSession) -> None:
    await async_client.post("/hero/", params={"name": "batman"})
    response = await async_client.get("/hero/", params={"name": "Batman", "intelligence": "<=90"})

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data) == 1

    response = await async_client.get("/hero/", params={"name": "Batman II", "intelligence": "<=90"})

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data) == 1
