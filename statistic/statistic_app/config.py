from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class MongoDBSettings(BaseModel):
    db_name: str = "fastapi_auth"
    collection_name: str = "data_objects"
    user: str = "user"
    password: str = "pass"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__"
    )

    mongo_db: MongoDBSettings = MongoDBSettings()


settings = Settings()
