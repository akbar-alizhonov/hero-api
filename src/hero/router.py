from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config.dependencies import get_async_session
from src.hero.repository import HeroRepository
from src.hero.schemas import HeroSchema
from src.hero.params import HeroParams
from src.hero.service import HeroService

router = APIRouter(tags=["Hero"], prefix="/hero")


@router.post(
    "/",
    response_model=list[HeroSchema],
    status_code=status.HTTP_200_OK,
    description="Создает новых героев в бд, если они найдены на сайте https://superheroapi.com/"
)
async def create_hero(
        name: str,
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    hero_repo = HeroRepository(session=session)
    hero_service = HeroService(repo=hero_repo)

    return await hero_service.create_hero_or_404(name)


@router.get(
    "/",
    response_model=list[HeroSchema],
    status_code=status.HTTP_200_OK,
    description=(
            "Возвращает всех героев с фильтрами. "
            "Фильтровать можно по имени и его характеристикам. "
            "ВАЖНО!!! Если вы фильтруете по характеристикам, "
            "то их можно указывать только в таким форматах <=100 или >=100 или 100 и тд."
    )
)
async def get_heroes(
        params: Annotated[HeroParams, Depends()],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        page: int = Query(1, ge=1, description="Номер страницы"),
        page_size: int = Query(20, ge=1, le=100, description="Количество элементов на странице")
):
    hero_repo = HeroRepository(session=session)
    hero_service = HeroService(repo=hero_repo)
    offset = (page - 1) * page_size

    return await hero_service.get_heroes(params, offset, page_size)
