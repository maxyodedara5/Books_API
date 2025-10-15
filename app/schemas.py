from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, conint


class BookBase(BaseModel):

    title: str
    author: str


class BookCreate(BookBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Book(BaseModel):
    id: int
    title: str
    author: str
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    Book: Book
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    book_id: int
    dir: Annotated[int, Field(strict=True, ge=0, le=1)]
