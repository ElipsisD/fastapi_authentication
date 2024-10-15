from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from auth.config import settings


class DatabaseManager:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            url=settings.db.url,
            echo=settings.db.echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


db_manager = DatabaseManager()
