from datetime import datetime

import pytest

from src.application.domain.model.account import AccountId
from src.application.domain.model.money import Money
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId
from src.application.port.inbound.send_money_use_case import (
    SendMoneyUseCase,
)
from src.adapter.inbound.web.send_money_controller import SendMoneyController
from src.application.port.inbound.send_money_command import SendMoneyCommand
from src.app import app


@pytest.fixture
def mock_send_money_use_case(mocker):
    mock_send_money_use_case = mocker.Mock(spec=SendMoneyUseCase)
    mock_send_money_use_case.send_money.return_value = Activity(
        id=ActivityId(1),
        owner_account_id=AccountId(41),
        source_account_id=AccountId(41),
        target_account_id=AccountId(42),
        timestamp=datetime.now(),
        money=Money.of(42),
    )
    return mock_send_money_use_case


@pytest.mark.asyncio
async def test_send_money(client, mock_send_money_use_case):
    with app.container.send_money_controller.override(  # type: ignore
        SendMoneyController(mock_send_money_use_case)
    ):
        response = await client.post(
            "/send-money",
            json={"source_account_id": 41, "target_account_id": 42, "amount": 42},
        )

    assert response.status_code == 200

    mock_send_money_use_case.send_money.assert_called_once_with(
        SendMoneyCommand(
            source_account_id=AccountId(41),
            target_account_id=AccountId(42),
            money=Money.of(42),
        )
    )


@pytest.mark.asyncio
async def test_send_money_failed(client):
    response = await client.post(
        "/send-money",
        json={"source_account_id": 41, "target_account_id": 42, "amount": 42},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Account with ID AccountId(41) not found."}
