from typing import Annotated

from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .api.users.schemas import UserCreateSchema, UserSchema
from .models import User, db_manager
from .utils.jwt import decode_jwt
from .utils.password import hash_password, validate_password
from .utils.user import get_user_by_username


async def get_user_data_for_registration(
    user_data: Annotated[UserCreateSchema, Depends()],
) -> UserSchema:
    password = hash_password(user_data.raw_password)
    return UserSchema(
        username=user_data.username,
        password=password,
        active=True,
    )


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> User:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := await get_user_by_username(username, session)):
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise unauthed_exc

    return user


def get_current_token_payload(
    token: str = Depends(oauth2_schema),
) -> str:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
        ) from None
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := await get_user_by_username(username, session):
        return UserSchema(
            username=user.username,
            password=user.password,
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


async def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
) -> UserSchema:
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )
