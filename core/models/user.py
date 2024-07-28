from sqlalchemy.orm import Mapped

from core.models.base import Base


class User(Base):
    username: Mapped[str]
    password: Mapped[str]
    active: Mapped[bool]
