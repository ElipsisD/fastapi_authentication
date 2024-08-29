from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.validation import get_current_active_auth_user, get_current_token_payload
from api.users import crud
from api.users.dependencies import get_user_data_for_registration
from api.users.schemas import UserResponseSchema, UserSchema
from core.models import User, db_manager

router = APIRouter(tags=["Users"])


@router.get("/me/")
async def get_user_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
) -> dict[str, bool | datetime | str]:
    iat = payload.get("iat")
    return {
        "username": user.username,
        "active": user.active,
        "logged_in": datetime.fromtimestamp(iat),
    }


@router.get(
    "/",
    response_model=list[UserResponseSchema],
)
async def get_all_users(
    user: UserSchema = Depends(get_current_active_auth_user),  # noqa: ARG001
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> list[User]:
    return await crud.get_users(session=session)


@router.post("/register/")
async def register_new_user(
    user_in: UserSchema = Depends(get_user_data_for_registration),
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> dict[str, str]:
    if await session.execute(select(User).filter_by(username=user_in.username)):
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
