from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.config import settings
from auth.models import User


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(tz=UTC)
    expire = (
        now + expire_timedelta
        if expire_timedelta
        else now + timedelta(minutes=expire_minutes)
    )
    to_encode.update(
        exp=expire,
        iat=now,
    )
    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> str:
    return jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


async def get_user_by_username(
    username: str,
    session: AsyncSession,
) -> User | None:
    stmt = select(User).filter(User.username == username)
    result: Result = await session.execute(stmt)
    return result.scalar_one()
