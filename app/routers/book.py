from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from database import get_db
import models, schemas

from fastapi import Depends, FastAPI, HTTPException, Response, status, APIRouter

from sqlalchemy.orm import Session
from typing import List
import oauth2



router = APIRouter(
    prefix="/books",
    tags=['Books']
)

@router.get("/", response_model=List[schemas.BookResponse])
def get_books(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    books = db.query(models.Book).all()
    return books


@router.get("/{id}", response_model=schemas.BookResponse)
def get_books(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    return book


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BookResponse)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    """
    Title:
    Author:
    """
    print(f"User : {current_user.email}")
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Book).filter(models.Book.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.BookResponse)
def update_book(id: int, book: schemas.BookBase, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    update_query = db.query(models.Book).filter(models.Book.id == id)
    if not update_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    
    update_query.update(book.model_dump(), synchronize_session=False)
    db.commit()

    return update_query.first()
