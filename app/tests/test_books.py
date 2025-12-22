import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import schemas
import pytest

def test_get_all_books(authenticated_client, test_books):
    res = authenticated_client.get("/books/")

    def validate(book):
        return schemas.BookResponse(**book)
    
    books_map = map(validate, res.json())
    # print(res.json())
    assert len(res.json()) == len(test_books)
    assert res.status_code == 200 

def test_unauthorized_user_get_all_books(client, test_books):
    res = client.get("/books/")
    assert res.status_code == 401

def test_unauthorized_user_get_book(client, test_books):
    res = client.get(f"/books/{test_books[0].id}")
    assert res.status_code == 401 

def test_get_book_not_exist(authenticated_client, test_books):
    res = authenticated_client.get("/books/798465123")
    assert res.status_code == 404


def test_get_one_book(authenticated_client, test_books):
    res = authenticated_client.get(f"/books/{test_books[0].id}")
    book = schemas.BookResponse(**res.json())
    assert book.Book.id == test_books[0].id
    assert book.Book.author == test_books[0].author
    assert book.Book.title == test_books[0].title

@pytest.mark.parametrize("title, author",
                         [
                             ("Title_One", "Author_One"),
                             ("Title_Two", "Author_Two"),
                             ("Title_Three", "Author_Three")
                         ])
def test_create_book(authenticated_client, test_user, test_books, title, author):
    res = authenticated_client.post(f"/books/", json={"title": title, "author": author})

    created_book = schemas.Book(**res.json())
    assert res.status_code == 201
    assert created_book.title == title
    assert created_book.author == author
    assert created_book.owner_id == test_user['id']

def test_unauthorized_user_create_book(client):
    res = client.post(f"/books/", json={"title": "Title_One", "author": "Author_One"})
    assert res.status_code == 401 

def test_unauthorized_user_delete_book(client, test_books):
    res = client.delete(f"/books/{test_books[0].id}")
    assert res.status_code == 401 

def test_delete_book(authenticated_client, test_user, test_books):
    res = authenticated_client.delete(f"/books/{test_books[0].id}")
    assert res.status_code == 204

def test_delete_non_existing_book(authenticated_client, test_user, test_books):
    res = authenticated_client.delete(f"/books/{12312123123}")
    assert res.status_code == 404

def test_delete_other_user_book(authenticated_client, test_user, test_books):
    res = authenticated_client.delete(f"/books/{test_books[2].id}")
    assert res.status_code == 403

def test_update_book(authenticated_client, test_user, test_books):
    data = {
        "title": "Book_Second_Updated",
        "author": "Author_Second_Updated"  
    }
    res = authenticated_client.put(f"/books/{test_books[0].id}", json=data)
    updated_book = schemas.BookBase(**res.json())
    assert res.status_code == 200
    assert updated_book.title == data["title"]
    assert updated_book.author == data["author"]

def test_update_other_user_book(authenticated_client, test_user, test_books, test_user2):
    data = {
            "title": "Book_Second_Updated",
            "author": "Author_Second_Updated"  
        }
    res = authenticated_client.put(f"/books/{test_books[2].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update(client, test_books):
    data = {
            "title": "Book_Second_Updated",
            "author": "Author_Second_Updated"  
        }
    res = client.put(f"/books/{test_books[0].id}", json=data)
    assert res.status_code == 401

def test_update_non_existing_book(authenticated_client, test_user, test_books):
    data = {
            "title": "Book_Second_Updated",
            "author": "Author_Second_Updated"  
        }
    res = authenticated_client.put(f"/books/{12312123123}", json=data)
    assert res.status_code == 404