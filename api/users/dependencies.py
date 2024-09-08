from typing import Annotated

from fastapi import Depends

from api.users.schemas import UserCreateSchema, UserSchema
from auth.utils import hash_password


async def get_user_data_for_registration(
    user_data: Annotated[UserCreateSchema, Depends()],
) -> UserSchema:
    password = hash_password(user_data.raw_password)
    return UserSchema(
        username=user_data.username,
        password=password,
        active=True,
    )
