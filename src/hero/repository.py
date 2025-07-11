from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.hero.schemas import HeroSchema
from src.hero.models import Hero


class HeroRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, hero: dict[str, str | int]) -> Hero:
        new_hero = Hero(**hero)
        self._session.add(new_hero)
        await self._session.commit()
        logger.info(f"Создан новый герой: {new_hero.name}, id: {new_hero.id}")

        return new_hero

    async def list(
            self,
            filters: list,
            limit: int,
            offset: int,
    ) -> list[Hero]:
        query = (
            select(Hero)
            .where(*filters)
            .limit(limit)
            .offset(offset)
        )
        res = await self._session.execute(query)

        return res.scalars().all()