import pytest

from src.application.domain.model.email import Email


def test_email_creation():
    email_address = "foo@example.com"
    email = Email(email_address)
    assert email.address == email_address
    assert str(email) == email_address


@pytest.mark.parametrize(
    "email",
    [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@domain..com",
    ],
)
def test_email_creation_invalid(email):
    with pytest.raises(ValueError, match="Invalid email address."):
        Email(email)
