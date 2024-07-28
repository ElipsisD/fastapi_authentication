from datetime import datetime

from fastapi import APIRouter, Depends
from api.users.schemas import UserSchema
from api.auth.validation import get_current_active_auth_user, get_current_token_payload

router = APIRouter(tags=["Users"])


@router.get("/users/me/")
def get_user_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "active": user.active,
        "logged_in": datetime.fromtimestamp(iat),
    }
