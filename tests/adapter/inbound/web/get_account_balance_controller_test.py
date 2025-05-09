import pytest

from src.application.domain.model.money import Money
from src.application.domain.model.account_id import AccountId
from src.application.port.inbound.get_account_balance_use_case import (
    GetAccountBalanceUseCase,
)
from src.adapter.inbound.web.get_account_balance_controller import (
    GetAccountBalanceController,
)
from src.application.port.inbound.get_account_balance_query import (
    GetAccountBalanceQuery,
)
from src.app import app


@pytest.fixture
def mock_get_account_balance_use_case(mocker):
    mock_get_account_balance_use_case = mocker.Mock(spec=GetAccountBalanceUseCase)
    mock_get_account_balance_use_case.get_account_balance.return_value = Money.of(42)
    return mock_get_account_balance_use_case


@pytest.mark.asyncio
async def test_get_account_balance(client, mock_get_account_balance_use_case):
    with app.container.get_account_balance_controller.override(  # type: ignore
        GetAccountBalanceController(mock_get_account_balance_use_case)
    ):
        response = await client.get("/account-balance/42")

    assert response.status_code == 200

    mock_get_account_balance_use_case.get_account_balance.assert_called_once_with(
        GetAccountBalanceQuery(account_id=AccountId(42))
    )
