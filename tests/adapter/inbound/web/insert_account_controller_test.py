import pytest

from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity_window import ActivityWindow
from src.application.domain.model.money import Money
from src.application.port.inbound.insert_account_use_case import (
    InsertAccountUseCase,
)
from src.adapter.inbound.web.insert_account_controller import InsertAccountController
from src.application.port.inbound.insert_account_command import InsertAccountCommand
from src.app import app


@pytest.fixture
def mock_insert_account_use_case(mocker):
    mock_insert_account_use_case = mocker.Mock(spec=InsertAccountUseCase)
    mock_insert_account_use_case.insert_account.return_value = Account(
        id=AccountId(42),
        baseline_balance=Money.of(42),
        activity_window=ActivityWindow([]),
    )
    return mock_insert_account_use_case


@pytest.mark.asyncio
async def test_insert_account(client, mock_insert_account_use_case):
    with app.container.insert_account_controller.override(  # type: ignore
        InsertAccountController(mock_insert_account_use_case)
    ):
        response = await client.post("/account", json={"account_id": 42, "amount": 42})

    assert response.status_code == 200

    mock_insert_account_use_case.insert_account.assert_called_once_with(
        InsertAccountCommand(account_id=AccountId(42), money=Money.of(42))
    )
