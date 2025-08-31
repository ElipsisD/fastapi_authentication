from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth_app.api.users import crud
from auth_app.api.users.schemas import UserResponseSchema
from auth_app.dependencies import get_current_active_auth_user, get_current_token_payload
from auth_app.models import User, db_manager

router = APIRouter(tags=["Users"])


@router.get("/me/")
async def get_user_info(
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_active_auth_user),
) -> dict[str, bool | datetime | str]:
    iat = payload.get("iat")
    return {
        "username": user.username,
        "active": user.active,
        "logged_in": datetime.fromtimestamp(iat),
    }


@router.get(
    "/",
    dependencies=[Depends(get_current_active_auth_user)],
    response_model=list[UserResponseSchema],
)
async def get_all_users(
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> list[User]:
    return await crud.get_users(session=session)
