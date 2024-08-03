from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.users import crud
from api.users.dependencies import get_user_data_for_registration
from api.users.schemas import UserResponseSchema, UserSchema
from api.auth.validation import get_current_active_auth_user, get_current_token_payload
from core.models import db_manager

router = APIRouter(tags=["Users"])


@router.get("/me/")
async def get_user_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
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
    user: UserSchema = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_manager.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.post("/register/")
async def register_new_user(
    user_in: UserSchema = Depends(get_user_data_for_registration),
    session: AsyncSession = Depends(db_manager.scoped_session_dependency),
):
    user = await crud.create_user(
        session=session,
        user_data=user_in,
    )
    return {
        "status": "success",
        "username": user.username,
    }
