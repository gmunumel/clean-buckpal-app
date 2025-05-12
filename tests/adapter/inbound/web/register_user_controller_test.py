import pytest

from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.status import Status
from src.application.port.inbound.register_user_use_case import (
    RegisterUserUseCase,
)
from src.adapter.inbound.web.register_user_controller import RegisterUserController
from src.application.port.inbound.register_user_command import RegisterUserCommand
from src.app import app


@pytest.fixture
def mock_register_user_use_case(mocker):
    mock_register_user_use_case = mocker.Mock(spec=RegisterUserUseCase)
    mock_register_user_use_case.register_user.return_value = User(
        id=UserId(1),
        name=Name("foo"),
        address=Address(
            street_name="bar",
            street_number=42,
            city="baz",
            postal_code="qux",
            country="tar",
        ),
        status=Status.enable(),
    )
    return mock_register_user_use_case


@pytest.mark.asyncio
async def test_register_user(client, mock_register_user_use_case):
    payload = {
        "user_id": 1,
        "name": "foo",
        "address": {
            "street_name": "bar",
            "street_number": 42,
            "city": "baz",
            "postal_code": "qux",
            "country": "tar",
        },
    }
    with app.container.register_user_controller.override(  # type: ignore
        RegisterUserController(mock_register_user_use_case)
    ):
        response = await client.post("/user", json=payload)

    assert response.status_code == 200

    mock_register_user_use_case.register_user.assert_called_once_with(
        RegisterUserCommand(
            user_id=UserId(1),
            user_name=Name("foo"),
            user_address=Address(
                street_name="bar",
                street_number=42,
                city="baz",
                postal_code="qux",
                country="tar",
            ),
        )
    )
