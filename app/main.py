from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str


@app.get("/")
async def read_root():
    return {"Hello": "World"}


books = [
    {
        "title": "A Walk to Remember",
        "author": "Nicholas Sparks",
        "id": 1
    },
    {
        "title": "The Night Circus",
        "author": "Erin Morgenstern",
        "id": 2
    },
]


def book_by_id(id):
    for book in books:
        if book["id"] == id:
            return book
    

def get_index(id):
    for index, book in enumerate(books):
        if book["id"] == id:
            return index

@app.get("/books")
def get_books():
    return {"Books": books}


@app.get("/books/{id}")
def get_books(id: int, response: Response):
    book = book_by_id(id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")

    return book
    


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_books(book: Book):
    """
    Title:
    Author:
    """
    new_book = book.model_dump()
    new_book["id"] = randrange(0,999)
    books.append(new_book)

    return {book.title: new_book}

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(id: int):
    index = get_index(id)
    books.pop(index)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/books/{id}")
def update_book(id: int, book: Book):
    index = get_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book Not Found Go Away, no id: {id} present")
    
    book_dict = book.model_dump()
    book_dict["id"] = id
    books[index] = book_dict

    return {"Updated book" : books[index]}