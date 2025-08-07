from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from os.path import join, dirname
from dotenv import load_dotenv
import time

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


DATABASE_PASSWORD = os.environ.get("PASSWORD")
USER = os.environ.get("USER")

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str


while True:
    try:
        conn = psycopg2.connect(host='localhost', database="books_db", user=USER, 
                                password=DATABASE_PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection successfully established")
        break
    except Exception as error:
        print("Connecting to DB failed:")
        print("Error: ", error)
        time.sleep(20)
        # TODO: Set a reasonable amount of time for sleep if DB connection not done


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/books")
def get_books():
    cursor.execute("""SELECT * from  books""")
    books = cursor.fetchall()
    return {"Books": books}


@app.get("/books/{id}")
def get_books(id: int):
    cursor.execute("""SELECT * FROM books where id = %s""", (str(id)))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    return {"Books": book}


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_books(book: Book):
    """
    Title:
    Author:
    """
    cursor.execute("""INSERT INTO books (title, author) VALUES (%s, %s) RETURNING *""", (book.title, book.author))
    new_book = cursor.fetchone()
    conn.commit()
    return {"Created Books": new_book}


@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(id: int):
    cursor.execute("""DELETE FROM books where id = %s RETURNING *""", (str(id)))
    deleted_book = cursor.fetchone()
    conn.commit()
    if not deleted_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    return {"Deleted Books": deleted_book}


@app.put("/books/{id}")
def update_book(id: int, book: Book):
    cursor.execute("""UPDATE books SET title = %s, author = %s where id = %s RETURNING *""", (book.title, book.author, str(id)))
    updated_book = cursor.fetchone()
    conn.commit()
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    return {"Updated Books": updated_book}
