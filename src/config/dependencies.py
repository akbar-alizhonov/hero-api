from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import async_session_maker


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()