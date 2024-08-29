from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.auth.validation import validate_auth_user
from api.users.schemas import UserSchema
from auth import utils as auth_utils

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
