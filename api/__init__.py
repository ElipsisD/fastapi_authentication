from fastapi import APIRouter

from .notes.views import router as note_router
from .auth.views import router as auth_router

router = APIRouter()
router.include_router(router=note_router, prefix="/notes")
router.include_router(router=auth_router, prefix="/auth")
