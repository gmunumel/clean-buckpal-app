import pytest

from src.application.port.inbound.login_user_command import LoginUserCommand
from src.application.domain.model.email import Email
from src.application.domain.model.password import Password


def test_login_user_command():
    email = Email("foo@example.com")
    password = Password("secret")

    command = LoginUserCommand(
        email=email,
        password=password,
    )

    assert command.email == email
    assert command.password == password


@pytest.mark.parametrize("email", ("", "foo", "foo@"))
def test_login_user_command_invalid_email(email):
    password = Password("secret")

    with pytest.raises(ValueError, match="Invalid email address."):
        email = Email(email)
        LoginUserCommand(
            email=email,
            password=password,
        )


def test_login_user_command_empty_email():
    password = Password("secret")

    with pytest.raises(ValueError, match="Email must be provided."):
        LoginUserCommand(
            email=None,  # type: ignore
            password=password,
        )
