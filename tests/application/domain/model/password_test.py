import pytest

from src.application.domain.model.password import Password


def test_password_creation():
    my_password = "securepassword123"
    password = Password(my_password)
    password_hash = password.hash()
    assert password.plain == my_password
    assert password_hash.verify(my_password)
    assert str(password) == my_password
    assert str(password_hash) == password_hash.hashed


def test_password_creation_empty_error():
    with pytest.raises(
        ValueError, match="Either plain or hashed password must be provided."
    ):
        Password()


def test_password_creation_both_given_error():
    with pytest.raises(ValueError, match="Only one of plain or hashed should be set."):
        Password("foo", "bar")
