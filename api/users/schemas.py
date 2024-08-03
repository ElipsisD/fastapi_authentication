from pydantic import BaseModel, ConfigDict


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    raw_password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    active: bool = True


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
