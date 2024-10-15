from fastapi import APIRouter

from .notes.views import router as note_router

router = APIRouter()
router.include_router(router=note_router, prefix="/notes")
