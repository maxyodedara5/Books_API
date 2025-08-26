from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional

class BookBase(BaseModel):

    title: str
    author: str

class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str
    author: str


class BookResponse(BookBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
