import aiohttp

from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import Hero
from src.config.settings import get_settings
from src.hero.filters import HeroFilter
from src.hero.repository import HeroRepository
from src.hero.schemas import HeroSchema


class HeroService:

    def __init__(self, session: AsyncSession, repo: HeroRepository) -> None:
        self.session = session
        self.repo = repo

    async def create_hero_or_404(self, name: str) -> Page[Hero]:
        settings = get_settings()
        url = (
            f"{settings.super_hero.SUPER_HERO_API}/"
            f"{settings.super_hero.SUPER_HERO_ACCESS_TOKEN}/"
            f"search/{name}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as resp:
                data: dict = await resp.json()

                if data.get("response") != "success":
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Герой не найден на superheroapi.com",
                    )

                for hero_data in data.get("results"):
                    hero = HeroSchema(**hero_data.get("powerstats"))
                    hero.name = hero_data.get("name")
                    await self.repo.create(hero.model_dump())

                await self.session.commit()

                filters = HeroFilter()
                filters.name = name
                query = self.repo.build_list_filtered_query(filters)

                return await paginate(self.session, query)

    async def get_heroes(self, hero_filter: HeroFilter) -> Page[Hero]:
        query = self.repo.build_list_filtered_query(hero_filter)
        return await paginate(self.session, query)
