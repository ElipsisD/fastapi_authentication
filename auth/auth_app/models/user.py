from sqlalchemy.orm import Mapped, mapped_column

from auth_app.models import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    active: Mapped[bool]
