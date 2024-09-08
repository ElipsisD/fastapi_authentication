from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.notes import crud
from api.notes.schemas import (
    NoteCreateSchema,
    NoteSchema,
    NoteUpdatePartialSchema,
    NoteUpdateSchema,
)
from core.models import Note, db_manager, mongo_db_manager
from .dependencies import note_by_id

router = APIRouter(tags=["Notes"])


@router.get("/", response_model=list[NoteSchemaSchema])
async def get_notes(
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> list[NoteSchema]:
    note_objects = await crud.get_notes(session)
    return [NoteSchema.model_validate(note) for note in note_objects]


@router.get("/{note_id}/", response_model=NoteSchema)
async def get_note(
    note: Note = Depends(note_by_id),
) -> NoteSchema:
    return NoteSchema.model_validate(note)


@router.post(
    "/",
    response_model=NoteSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    note_data: Annotated[NoteCreateSchema, Depends()],
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> NoteSchema | None:
    note = await crud.create_note(session, note_data)
    return NoteSchema.model_validate(note)


@router.put("/{note_id}/")
async def update_note(
    note_data: Annotated[NoteUpdateSchema, Depends()],
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> NoteSchema:
    note = await crud.update_note(
        session=session,
        note=note,
        note_data=note_data,
    )
    return NoteSchema.model_validate(note)


@router.patch("/{note_id}/")
async def partial_update_note(
    note_data: Annotated[NoteUpdatePartialSchema, Depends()],
    note: Note = Depends(note_by_id),
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> NoteSchema:
    note = await crud.update_note(
        session=session,
        note=note,
        note_data=note_data,
        partial=True,
    )
    return NoteSchema.model_validate(note)


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
