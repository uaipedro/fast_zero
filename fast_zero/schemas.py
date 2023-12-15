from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


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
