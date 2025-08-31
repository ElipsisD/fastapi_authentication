from datetime import UTC, datetime, timedelta

import jwt

from auth_app.config import settings


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
