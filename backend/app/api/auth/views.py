from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.auth.validation import validate_auth_user
from app.api.users import crud
from app.api.users.dependencies import get_user_data_for_registration
from app.api.users.schemas import UserSchema
from app.auth import utils as auth_utils
from app.models import User, db_manager

router = APIRouter(tags=["JWTAuth"])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
) -> TokenInfo:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    access_token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",  # noqa: S106
    )


@router.post("/register/")
async def register_new_user(
    user_in: UserSchema = Depends(get_user_data_for_registration),
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> dict[str, str]:
    user_exists = await session.execute(
        select(exists().where(User.username == user_in.username))
    )
    if user_exists.scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same 'username' already registered",
        )

    user = await crud.create_user(
        session=session,
        user_data=user_in,
    )
    return {
        "status": "success",
        "username": user.username,
    }
