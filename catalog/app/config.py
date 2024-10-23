from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "data" / "db.sqlite"


class RabbitSettings(BaseModel):
    user: str = "guest"
    password: str = "guest"
    path: str = f"amqp://{user}:{password}@ms.rabbitmq:5672/"


class DBSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    echo: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__"
    )

    db: DBSettings = DBSettings()
    rabbit_mq: RabbitSettings = RabbitSettings()


settings = Settings()
