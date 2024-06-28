from uuid import UUID

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USER: str = "default"
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0

    POSTGRES_DSN: str = "postgresql://postgres:postgres@localhost:5432/postgres"

    NOTION_API_KEY: str = ""
    NOTION_ROOT_PAGE_ID: UUID = ""
    DEFAULT_AUTHOR_ID: UUID = ""

    ENVIRONMENT: str = "local"


settings = Settings()
