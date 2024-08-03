from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from api.auth.utils import get_user_by_username
from api.users.schemas import UserSchema
from auth import utils as auth_utils

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login/"
)


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := await get_user_by_username(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise unauthed_exc

    return user


def get_current_token_payload(
    token: str = Depends(oauth2_schema),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := await get_user_by_username(username):
        return UserSchema(
            username=user.username,
            password=user.password,
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


async def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )
