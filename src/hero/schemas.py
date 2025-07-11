from pydantic import BaseModel, field_validator


class HeroSchema(BaseModel):
    name: str | None = None
    intelligence: int | None = None
    strength: int | None = None
    speed: int | None = None
    durability: int | None = None
    power: int | None = None
    combat: int | None = None

    @field_validator("*", mode="before")
    @classmethod
    def convert_str_to_int(cls, value: str | int | None):
        if not value:
            return None

        if isinstance(value, int):
            return value

        if value.isdigit():
            return int(value)

        return value
