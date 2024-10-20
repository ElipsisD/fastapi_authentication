from fastapi import APIRouter

from .auth.views import router as auth_router
from .users.views import router as users_router

router = APIRouter()
router.include_router(router=auth_router)
router.include_router(router=users_router, prefix="/users")


@router.get("/health-check/")
async def health_check() -> bool:
    return True
