from .. import schemas
import pytest
from config import settings
from jose import jwt
 


def test_create_user(client, test_user):
    res = client.post("/users/", json={"email": "test_user@book.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test_user@book.com"
    assert res.status_code == 201

def test_user_login(client, test_user):
    res = client.post("/login/", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@book.com", "password123", 403),
    ("rightemail@book.com", "password", 403),
    ("wrongemail@book.com", "password", 403),
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login/", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"


@pytest.mark.parametrize("email, password, status_code", [
    (None, "password", 422),
    ("wrongemail@book.com", None, 422),
])
def test_incorrect_login_without_fields(client, email, password, status_code):
    if email == None:
        res = client.post("/login/", data={"password": password})
    
    if password == None:
        res = client.post("/login/", data={"username": email})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
    