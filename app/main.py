import os
import time
from os.path import dirname, join

from typing import List
import models
import psycopg2
import schemas
from database import engine, get_db
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

# from . import models, schemas
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


DATABASE_PASSWORD = os.environ.get("PASSWORD")
USER = os.environ.get("USER")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/books", response_model=List[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


@app.get("/books/{id}", response_model=schemas.BookResponse)
def get_books(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    return book


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=schemas.BookResponse)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Title:
    Author:
    """
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Book).filter(models.Book.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/books/{id}", response_model=schemas.BookResponse)
def update_book(id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    
    update_query = db.query(models.Book).filter(models.Book.id == id)
    if not update_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    
    update_query.update(book.model_dump(), synchronize_session=False)
    db.commit()

    return update_query.first()

