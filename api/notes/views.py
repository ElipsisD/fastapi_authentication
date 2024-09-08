from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import note_by_id
from core.models import db_manager
from api.notes import crud
from api.notes.schemas import Note, NoteCreate, NoteUpdate, NoteUpdatePartial

router = APIRouter(tags=["Notes"])


@router.get("/", response_model=list[Note])
async def get_notes(
    session: AsyncSession = Depends(db_manager.session_dependency),
):
    return await crud.get_notes(session)


@router.get("/{note_id}/", response_model=Note)
async def get_note(
    note: Note = Depends(note_by_id),
):
    return note


@router.post(
    "/",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    note_data: Annotated[NoteCreateSchema, Depends()],
    session: AsyncSession = Depends(db_manager.session_dependency),
):
    return await crud.create_note(session, note_data)


@router.put("/{note_id}/")
async def update_note(
    note_data: Annotated[NoteUpdateSchema, Depends()],
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_manager.session_dependency),
):
    return await crud.update_note(
        session=session,
        note=note,
        note_data=note_data,
    )


@router.patch("/{note_id}/")
async def partial_update_note(
    note_data: Annotated[NoteUpdatePartialSchema, Depends()],
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_manager.session_dependency),
):
    return await crud.update_note(
        session=session,
        note=note,
        note_data=note_data,
        partial=True,
    )


@router.delete(
    "/{note_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> None:
    await crud.delete_note(
        session=session,
        note=note,
    )
