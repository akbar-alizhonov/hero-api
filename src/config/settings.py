from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseCustomSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SuperHeroSettings(BaseCustomSettings):
    SUPER_HERO_ACCESS_TOKEN: str = Field("access_token")
    SUPER_HERO_API: str = Field("")


class PostgresSettings(BaseCustomSettings):
    DB_HOST: str = Field("localhost")
    DB_PORT: int = Field(5432)
    DB_DATABASE: str = Field("postgres")
    DB_USER: str = Field("postgres")
    DB_PASSWORD: str = Field("postgres")

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"


class LoggingSettings(BaseCustomSettings):
    DEVELOPMENT: bool = False
    LOG_LEVEL: str = Field("INFO")


class Settings:
    db = PostgresSettings()
    super_hero = SuperHeroSettings()
    logging = LoggingSettings()


def get_settings():
    return Settings()
