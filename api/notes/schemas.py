from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteBaseSchema(BaseModel):
    text: str
    created_at: datetime
    active: bool


class NoteCreateSchema(NoteBaseSchema):
    pass


class NoteUpdateSchema(NoteCreateSchema):
    pass


class NoteUpdatePartialSchema(NoteCreateSchema):
    text: str | None = None
    created_at: datetime | None = None
    active: bool | None = None


class NoteSchemaSchema(NoteBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
