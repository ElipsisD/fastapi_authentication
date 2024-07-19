from datetime import datetime

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class Note(Base):
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime]
    active: Mapped[bool]
