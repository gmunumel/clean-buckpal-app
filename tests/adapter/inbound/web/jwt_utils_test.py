import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from src.adapter.inbound.web.jwt_utils import create_jwt_token, authenticate_user
from src.common.config import SECRET_KEY, ALGORITHM, DUMMY_EMAIL, DUMMY_USER


class DummyUserRepository:
    def __init__(self, user=None):
        self._user = user

    def find_by_id(self, _user_id):
        return self._user


def make_token(user_id="123", email="foo@example.com"):
    payload = {"sub": user_id, "email": email}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def make_credentials(token):
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def test_jwt_utils_create_jwt_token():
    token = create_jwt_token(DUMMY_USER)
    assert token is not None
    assert isinstance(token, str)


def test_jwt_utils_authenticate_user_valid():
    dummy_user = object()
    repo = DummyUserRepository(user=dummy_user)
    token = make_token(user_id="123", email="foo@example.com")
    credentials = make_credentials(token)

    result = authenticate_user(credentials=credentials, user_repository=repo)  # type: ignore
    assert result == dummy_user


def test_jwt_utils_authenticate_user_dummy_email():
    repo = DummyUserRepository(user=None)
    token = make_token(user_id="1", email=DUMMY_EMAIL)
    credentials = make_credentials(token)

    result = authenticate_user(credentials=credentials, user_repository=repo)  # type: ignore
    assert result == DUMMY_USER


def test_jwt_utils_authenticate_user_invalid_token():
    repo = DummyUserRepository(user=None)
    credentials = make_credentials("invalid.token.value")
    with pytest.raises(HTTPException) as excinfo:
        authenticate_user(credentials=credentials, user_repository=repo)  # type: ignore
    assert excinfo.value.status_code == 401


def test_jwt_utils_authenticate_user_user_not_found():
    repo = DummyUserRepository(user=None)
    token = make_token(user_id="999", email="foo@example.com")
    credentials = make_credentials(token)
    with pytest.raises(HTTPException) as excinfo:
        authenticate_user(credentials=credentials, user_repository=repo)  # type: ignore
    assert excinfo.value.status_code == 401


def test_jwt_utils_authenticate_user_missing_sub():
    repo = DummyUserRepository(user=None)
    payload = {"email": "foo@example.com"}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    credentials = make_credentials(token)
    with pytest.raises(HTTPException) as excinfo:
        authenticate_user(credentials=credentials, user_repository=repo)  # type: ignore
    assert excinfo.value.status_code == 401
