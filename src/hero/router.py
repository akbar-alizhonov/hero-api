from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from starlette import status

from src.config.dependencies import get_async_session
from src.hero.filters import HeroFilter
from src.hero.repository import HeroRepository
from src.hero.schemas import HeroSchema
from src.hero.service import HeroService

router = APIRouter(tags=["Hero"], prefix="/hero")


@router.post(
    "/",
    response_model=Page[HeroSchema],
    status_code=status.HTTP_200_OK,
    description="Создает новых героев в бд, если они найдены на сайте https://superheroapi.com/"
)
async def create_hero(
    name: str,
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    hero_repo = HeroRepository(session=session)
    hero_service = HeroService(session=session, repo=hero_repo)

    heroes = await hero_service.create_hero_or_404(name)
    return heroes


@router.get(
    "/",
    response_model=Page[HeroSchema],
    status_code=status.HTTP_200_OK,
    description=(
            "Возвращает всех героев с фильтрами. "
            "Фильтровать можно по имени и его характеристикам. "
            "ВАЖНО!!! Если вы фильтруете по характеристикам, "
            "то их можно указывать только в таким форматах <=100 или >=100 или 100 и тд."
    )
)
async def get_heroes(
    hero_filter: Annotated[HeroFilter, FilterDepends(HeroFilter)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    hero_repo = HeroRepository(session=session)
    hero_service = HeroService(session=session, repo=hero_repo)

    result = await hero_service.get_heroes(hero_filter)
    if not result.items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найдено героев с такими фильтрами"
        )

    return result
