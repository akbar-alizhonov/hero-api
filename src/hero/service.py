import aiohttp

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import Hero
from src.config.settings import get_settings
from src.hero.params import HeroParams
from src.hero.repository import HeroRepository
from src.hero.schemas import HeroSchema


class HeroService:

    def __init__(self, repo: HeroRepository) -> None:
        self.repo = repo

    async def create_hero_or_404(self, name: str) -> list[Hero]:
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

                res = []

                for hero_data in data.get("results"):
                    hero = HeroSchema(**hero_data.get("powerstats"))
                    hero.name = hero_data.get("name")
                    new_hero = await self.repo.create(hero.model_dump())
                    res.append(new_hero)

                return res

    async def get_heroes(self, params: HeroParams, offset: int, limit: int) -> list[Hero]:
        filters = []

        if params.name:
            filters.append(Hero.name == params.name)

        numeric_fields = {
            "intelligence": params.intelligence,
            "strength": params.strength,
            "speed": params.speed,
            "power": params.power,
            "durability": params.durability,
            "combat": params.combat,
        }

        for field, value in numeric_fields.items():
            if value is not None:
                col = getattr(Hero, field)

                if value.isdigit():  # Точное совпадение
                    filters.append(col == int(value))
                else:  # Операторы сравнения
                    op = value[:2]
                    num = int(value[2:])

                    if op == ">=":
                        filters.append(col >= num)
                    elif op == "<=":
                        filters.append(col <= num)

        heroes = await self.repo.list(filters, limit, offset)
        if not heroes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не найдено героев с такими фильтрами"
            )

        return heroes



