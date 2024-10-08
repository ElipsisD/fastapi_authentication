from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


async def get_user_by_username(
    username: str,
    session: AsyncSession,
) -> User | None:
    stmt = select(User).filter(User.username == username)
    result: Result = await session.execute(stmt)
    return result.scalar_one()
