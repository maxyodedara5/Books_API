from pydantic import BaseModel
from datetime import datetime

class BookBase(BaseModel):
    id: int
    title: str
    author: str

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    created_at: datetime

    class Config:
        from_attributes = True

