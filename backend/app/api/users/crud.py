from fastapi import Depends
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.schemas import UserSchema
from app.models import User, db_manager


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def create_user(
    user_data: UserSchema,
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> User:
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    return user
