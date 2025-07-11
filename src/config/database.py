from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config.settings import get_settings


def get_async_engine() -> AsyncEngine:
    settings = get_settings()
    engine = create_async_engine(settings.db.url)
    return engine


def get_async_session_maker() -> sessionmaker:
    engine = get_async_engine()
    session_maker = sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
    return session_maker

async_session_maker = get_async_session_maker()
