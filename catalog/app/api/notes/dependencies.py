from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Note, db_manager

from . import crud


async def note_by_id(
    note_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_manager.session_dependency),
) -> Note:
    note = await crud.get_note(session, note_id)
    if note is not None:
        return note

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Note not found!",
    )
