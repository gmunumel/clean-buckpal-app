import pytest

from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity_window import ActivityWindow
from src.application.domain.model.money import Money
from src.application.port.inbound.update_account_use_case import (
    UpdateAccountUseCase,
)
from src.adapter.inbound.web.update_account_controller import UpdateAccountController
from src.application.port.inbound.update_account_command import UpdateAccountCommand
from src.app import app


@pytest.fixture
def mock_update_account_use_case(mocker):
    mock_update_account_use_case = mocker.Mock(spec=UpdateAccountUseCase)
    mock_update_account_use_case.update_account.return_value = Account(
        id=AccountId(42),
        baseline_balance=Money.of(42),
        activity_window=ActivityWindow([]),
    )
    return mock_update_account_use_case


@pytest.mark.asyncio
async def test_update_account(client, mock_update_account_use_case):
    with app.container.update_account_controller.override(  # type: ignore
        UpdateAccountController(mock_update_account_use_case)
    ):
        response = await client.put("/account/42", json={"amount": 42})

    assert response.status_code == 201

    mock_update_account_use_case.update_account.assert_called_once_with(
        UpdateAccountCommand(account_id=AccountId(42), money=Money.of(42))
    )
