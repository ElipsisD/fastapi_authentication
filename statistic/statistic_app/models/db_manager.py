from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from statistic_app.config import settings


class DBManager:
    def __init__(self) -> None:
        url = f"mongodb://{settings.mongo_db.user}:{settings.mongo_db.password}@mongo_db:27017"
        self._client = AsyncIOMotorClient(url)
        self._db = self._client[settings.mongo_db.db_name]
        self.collection = self._db[settings.mongo_db.collection_name]

    def get_connect(self) -> AsyncIOMotorCollection:
        yield self.collection


db_manager = DBManager()
