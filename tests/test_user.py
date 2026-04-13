from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Тестовые данные
users = [
    {'id': 1, 'name': 'Ivan Ivanov', 'email': 'i.i.ivanov@mail.com'},
    {'id': 2, 'name': 'Petr Petrov', 'email': 'p.p.petrov@mail.com'}
]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': 'no@mail.com'})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_user_with_valid_email():
    new_user = {"name": "Sergey Sergeev", "email": "sergey@mail.com"}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

def test_create_user_with_invalid_email():
    existed_user = {"name": "Duplicate", "email": users[0]["email"]}
    response = client.post("/api/v1/user", json=existed_user)
    assert response.status_code == 409
    assert response.json()["detail"] == "User with this email already exists"

def test_delete_user():
    new_user = {"name": "To Delete", "email": "delete@mail.com"}
    client.post("/api/v1/user", json=new_user)
    response = client.delete("/api/v1/user", params={'email': new_user["email"]})
    assert response.status_code == 204

