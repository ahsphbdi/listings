from fastapi.testclient import TestClient

from app.tests.override import TestingSessionLocal
from app.tests.utils.utils import get_serializable_random_user, random_email
from app.main import app
from app.crud.user import get_user_by_email

client = TestClient(app)


def test_register():
    db = TestingSessionLocal()
    user_in = get_serializable_random_user()
    response = client.post(
        "/auth/register/",
        json=user_in
    )
    db.close()
    user_db = get_user_by_email(db, user_in['email'])
    assert response.status_code == 201
    assert user_db.username == user_in['username']


def test_register_existing_username_email():
    db = TestingSessionLocal()
    user_in = get_serializable_random_user()
    response = client.post(
        "/auth/register/",
        json=user_in
    )
    user_in['email'] = random_email()
    response_exising_username = client.post(
        "/auth/register/",
        json=user_in
    )
    db.close()
    assert response.status_code == 201
    assert response_exising_username.status_code == 406


def test_login():
    db = TestingSessionLocal()
    user_in = get_serializable_random_user()
    response = client.post(
        "/auth/register/",
        json=user_in
    )
    login_response = client.post(
        "/auth/token/",
        json={
            'username': user_in['username'],
            'email':    user_in['email'],
            'password': user_in['password1']
        }
    )
    db.close()
    assert response.status_code==201
    assert login_response.status_code==200


def test_no_login():
    db = TestingSessionLocal()
    user_in = get_serializable_random_user()
    response = client.post(
        "/auth/register/",
        json=user_in
    )
    login_response = client.post(
        "/auth/token/",
        json={
            'username': user_in['username'],
            'email':    user_in['email'],
            'password': user_in['password1']+' fake'
        }
    )
    db.close()
    assert response.status_code==201
    assert login_response.status_code==401
