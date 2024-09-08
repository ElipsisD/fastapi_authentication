from typing import TYPE_CHECKING

from sqlalchemy import Result, select

from core.models import User, db_manager

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_username(username: str) -> User | None:
    session: AsyncSession = db_manager.session_factory()
    stmt = select(User).filter(User.username == username)
    result: Result = await session.execute(stmt)
    return result.scalar_one()

