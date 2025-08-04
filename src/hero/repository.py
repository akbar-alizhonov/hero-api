from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.hero.models import Hero
from src.hero.filters import HeroFilter

class HeroRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, hero: dict[str, str | int]) -> Hero:
        new_hero = Hero(**hero)
        self._session.add(new_hero)
        await self._session.flush()

        logger.info(f"Создан новый герой: {new_hero.name}, id: {new_hero.id}")
        return new_hero

    @staticmethod
    def build_list_filtered_query(hero_filter: HeroFilter):
        """Строит SQLAlchemy запрос с фильтрами"""
        query = select(Hero)
        query = hero_filter.filter(query)
        query = hero_filter.sort(query)

        return query