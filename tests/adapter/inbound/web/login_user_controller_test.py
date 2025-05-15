import pytest

from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.status import Status
from src.application.domain.model.email import Email
from src.application.domain.model.password import Password
from src.application.port.inbound.login_user_use_case import LoginUserUseCase
from src.adapter.inbound.web.login_user_controller import LoginUserController
from src.application.port.inbound.login_user_command import LoginUserCommand
from src.app import app


@pytest.fixture
def mock_login_user_use_case(mocker):
    mock_login_user_use_case = mocker.Mock(spec=LoginUserUseCase)
    mock_login_user_use_case.login_user.return_value = User(
        id=UserId(1),
        name=Name("foo"),
        email=Email("foo@example.com"),
        password=Password("secret"),
        address=Address(
            street_name="bar",
            street_number=42,
            city="baz",
            postal_code="qux",
            country="tar",
        ),
        status=Status.enable(),
    )
    return mock_login_user_use_case


@pytest.mark.asyncio
async def test_login_user(client, mock_login_user_use_case):
    payload = {
        "user_id": 1,
        "name": "foo",
        "email": "foo@example.com",
        "password": "secret",
        "address": {
            "street_name": "bar",
            "street_number": 42,
            "city": "baz",
            "postal_code": "qux",
            "country": "tar",
        },
    }
    with app.container.login_user_controller.override(  # type: ignore
        LoginUserController(mock_login_user_use_case)
    ):
        response = await client.post("/login", json=payload)

    assert response.status_code == 200

    mock_login_user_use_case.login_user.assert_called_once_with(
        LoginUserCommand(
            email=Email("foo@example.com"),
            password=Password("secret"),
        )
    )
