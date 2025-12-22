import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.testclient import TestClient
from alembic import command

from oauth2 import create_access_token


# Using relative imports ..config or ..database will for some reason
# stop the app dependency from overriding

from main import app
# from .. import schemas
from config import settings
from database import Base, get_db
import models

TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"
test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Base.metadata.create_all(bind=test_engine)
# client = TestClient(app)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email":"testuser@book.com",
                 "password":"password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"testuser2@book.com",
                 "password":"password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authenticated_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_books(test_user, test_user2, session):
    books_data = [{
        "title": "Book_First",
        "author": "Author_First",
        "owner_id": test_user["id"]
    }, {
        "title": "Book_Second",
        "author": "Author_Second",
        "owner_id": test_user["id"]
    }, {
        "title": "Book_Third",
        "author": "Author_Third",
        "owner_id": test_user2["id"]
    }]

    def create_book_model(books_data):
        return models.Book(**books_data)

    book_map = map(create_book_model, books_data)
    books_list = list(book_map)


    session.add_all(books_list)

    # session.add_all([models.Book])
    session.commit()
    created_books = session.query(models.Book).all()


    return created_books

