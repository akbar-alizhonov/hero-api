from sqlalchemy.orm import Mapped, mapped_column

from src.config.base import Base


class Hero(Base):
    __tablename__ = 'hero'
    __table_args__ = {
        "comment": "Таблица с героями и их характеристиками"
    }

    name: Mapped[str] = mapped_column(nullable=False, comment="Имя героя", index=True)
    intelligence: Mapped[int] = mapped_column(nullable=False, comment="Интеллект")
    strength: Mapped[int] = mapped_column(nullable=False, comment="Сила")
    speed: Mapped[int] = mapped_column(nullable=False, comment="Скорость")
    durability: Mapped[int] = mapped_column(nullable=False, comment="Выносливость")
    power: Mapped[int] = mapped_column(nullable=False, comment="Мощь")
    combat: Mapped[int] = mapped_column(nullable=False, comment="Битва")