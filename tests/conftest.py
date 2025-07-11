import asyncio
from typing import Generator, Callable

import pytest
import pytest_asyncio
from fastapi import FastAPI

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.base import Base
from src.config.database import async_session_maker, get_async_engine


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    engine = get_async_engine()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

        async with async_session_maker(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture()
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from src.config.dependencies import get_async_session
    from src.main import app

    app.dependency_overrides[get_async_session] = override_get_db
    return app


@pytest_asyncio.fixture()
async def async_client(app: FastAPI):
    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test"
    ) as ac:
        yield ac