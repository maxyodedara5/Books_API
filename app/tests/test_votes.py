import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import models

import pytest

@pytest.fixture()
def test_vote(test_books, session, test_user):
    new_vote = models.Vote(book_id=test_books[2].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()



def test_vote_on_book(authenticated_client, test_books):
    res = authenticated_client.post("/vote/", json={"book_id": test_books[2].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_book(authenticated_client, test_books, test_vote):
    res = authenticated_client.post("/vote/", json={"book_id": test_books[2].id, "dir": 1})
    assert res.status_code == 409

def test_vote_delete(authenticated_client, test_books, test_vote):
    res = authenticated_client.post("/vote/", json={"book_id": test_books[2].id, "dir": 0})
    assert res.status_code == 201

def test_delete_vote_not_present(authenticated_client, test_books):
    res = authenticated_client.post("/vote/", json={"book_id": test_books[0].id, "dir": 0})
    assert res.status_code == 404

def test_vote_book_not_present(authenticated_client, test_books):
    res = authenticated_client.post("/vote/", json={"book_id": 123123123, "dir": 1})
    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_books):
    res = client.post("/vote/", json={"book_id": test_books[0].id, "dir": 1})
    assert res.status_code == 401
