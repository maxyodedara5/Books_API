from typing import List

import database
import models
from config import settings
from fastapi import Depends, FastAPI, HTTPException, Response, status
from routers import auth, book, user, vote
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
