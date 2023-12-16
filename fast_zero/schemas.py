from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserPartial(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic] = []


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str
