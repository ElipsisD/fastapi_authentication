from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    active: Mapped[bool]
