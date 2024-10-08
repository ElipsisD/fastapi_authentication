from fastapi import APIRouter

from .auth.views import router as auth_router
from .notes.views import router as note_router
from .users.views import router as users_router

router = APIRouter()
router.include_router(router=note_router, prefix="/notes")
router.include_router(router=auth_router, prefix="/auth")
router.include_router(router=users_router, prefix="/users")
