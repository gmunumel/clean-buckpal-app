import pytest

from src.application.domain.model.user_id import UserId


def test_user_id_equality():
    user_id1 = UserId(1)
    user_id2 = UserId(1)
    user_id3 = UserId(2)

    assert user_id1 == user_id2
    assert user_id1 != user_id3
    assert user_id2 != user_id3


def test_user_id_invalid_value():
    match = "UserId must be a positive integer."
    with pytest.raises(ValueError, match=match):
        UserId(-1)  # type: ignore
    with pytest.raises(ValueError, match=match):
        UserId(0)  # type: ignore
    with pytest.raises(ValueError, match=match):
        UserId("invalid")  # type: ignore
