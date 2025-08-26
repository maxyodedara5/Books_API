
from typing import List

import models
import database

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from routers import book, user, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(book.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}






