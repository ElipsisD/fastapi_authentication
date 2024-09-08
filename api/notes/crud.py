from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.notes.schemas import NoteCreate, NoteUpdate, NoteUpdatePartial
from core.models import Note


async def get_notes(session: AsyncSession) -> list[Note]:
    stmt = select(Note)
    result: Result = await session.execute(stmt)
    notes = result.scalars().all()
    return list(notes)


async def get_note(session: AsyncSession, note_id: int) -> Note | None:
    return await session.get(Note, note_id)


async def create_note(session: AsyncSession, note_data: NoteCreate) -> Note | None:
    note = Note(**note_data.model_dump())
    session.add(note)
    await session.commit()
    return note


async def update_note(
    session: AsyncSession,
    note: Note,
    note_data: NoteUpdate | NoteUpdatePartial,
    *,
    partial: bool = False,
) -> Note:
    for name, value in note_data.model_dump(exclude_none=partial).items():
        setattr(note, name, value)
    await session.commit()
    return note


async def delete_note(
    session: AsyncSession,
    note: Note,
) -> None:
    await session.delete(note)
    await session.commit()
