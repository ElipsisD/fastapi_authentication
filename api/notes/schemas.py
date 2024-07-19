from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    text: str
    created_at: datetime
    active: bool


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteCreate):
    pass


class NoteUpdatePartial(NoteCreate):
    text: str | None = None
    created_at: datetime | None = None
    active: bool | None = None


class Note(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
