import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from typing import List, Optional

import models, oauth2, schemas
from database import get_db
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    book = db.query(models.Book).filter(models.Book.id == vote.book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book ID: {vote.book_id} not found",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.book_id == vote.book_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} already voted for book id {vote.book_id}",
            )

        new_vote = models.Vote(book_id=vote.book_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added Vote"}
    if vote.dir == 0:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found"
            )

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Sucessfully removed Vote"}
