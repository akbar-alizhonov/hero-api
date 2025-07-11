from pydantic import BaseModel, field_validator


class HeroParams(BaseModel):
    name: str | None = None
    intelligence: str | None = None
    strength: str | None = None
    speed: str | None = None
    durability: str | None = None
    power: str | None = None
    combat: str | None = None

    @field_validator(
        "intelligence",
        "strength",
        "speed",
        "durability",
        "power",
        "combat",
        mode="before",
    )
    @classmethod
    def validate_numeric_filter(cls, value: str | None) -> str | None:
        if value is None:
            return None

        if value.startswith((">=", "<=")):
            return value

        if value.isdigit():
            return value

        if value.isalpha():
            return value

        raise ValueError("Некорректный формат фильтра. Используйте число или операторы: >=, <=")
