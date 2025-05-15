from src.application.port.inbound.register_user_command import RegisterUserCommand
from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.email import Email
from src.application.domain.model.password import Password


def test_register_user_command():
    user_id = UserId(1)
    name = Name("foo")
    email = Email("foo@example.com")
    password = Password("secret")
    address = Address(
        street_name="foo",
        street_number=42,
        city="bar",
        postal_code="baz",
        country="qux",
    )

    command = RegisterUserCommand(
        user_id=user_id,
        user_name=name,
        user_email=email,
        user_password=password,
        user_address=address,
    )

    assert command.user_id == user_id
    assert command.user_name == name
    assert command.user_address == address
    assert command.user_email == email
    assert command.user_password == password
