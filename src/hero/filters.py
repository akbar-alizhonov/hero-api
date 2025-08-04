from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from typing import Optional, List

from src.hero.models import Hero


class HeroFilter(Filter):
    name: Optional[str] = None
    name__ilike: Optional[str] = Field(None, alias="name_ilike")
    intelligence__gte: Optional[int] = None
    intelligence__lte: Optional[int] = None
    strength__gte: Optional[int] = None
    strength__lte: Optional[int] = None
    speed__gte: Optional[int] = None
    speed__lte: Optional[int] = None
    power__gte: Optional[int] = None
    power__lte: Optional[int] = None
    durability__gte: Optional[int] = None
    durability__lte: Optional[int] = None
    combat__gte: Optional[int] = None
    combat__lte: Optional[int] = None

    order_by: Optional[List[str]] = Field(None, alias="order_by")

    class Constants(Filter.Constants):
        model = Hero
        ordering_field_name = "order_by"
        ordering_model_fields = [
            "name", "intelligence", "strength",
            "speed", "power", "durability", "combat"
        ]