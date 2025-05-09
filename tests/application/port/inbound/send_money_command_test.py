import pytest

from src.application.port.inbound.send_money_command import SendMoneyCommand
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money


def test_send_money_command():
    source_account_id = AccountId(1)
    target_account_id = AccountId(2)
    money = Money.of(float("inf"))

    command = SendMoneyCommand(
        source_account_id=source_account_id,
        target_account_id=target_account_id,
        money=money,
    )

    assert command.source_account_id == source_account_id
    assert command.target_account_id == target_account_id
    assert command.money == money


def test_send_money_command_money_validation_fails():
    source_account_id = AccountId(1)
    target_account_id = AccountId(2)
    money = Money.of(-10)

    with pytest.raises(ValueError, match="Money amount must be greater than zero."):
        SendMoneyCommand(
            source_account_id=source_account_id,
            target_account_id=target_account_id,
            money=money,
        )


def test_send_money_command_account_id_validation_fails():
    source_account_id = AccountId(1)
    target_account_id = None
    money = Money.of(10)

    with pytest.raises(
        ValueError, match="Source and target account IDs must be provided."
    ):
        SendMoneyCommand(
            source_account_id=source_account_id,
            target_account_id=target_account_id,  # type: ignore
            money=money,
        )


def test_send_money_command_validation_fails_with_no_money():
    source_account_id = AccountId(1)
    target_account_id = AccountId(2)
    money = None

    with pytest.raises(ValueError, match="Money amount must be provided."):
        SendMoneyCommand(
            source_account_id=source_account_id,
            target_account_id=target_account_id,
            money=money,  # type: ignore
        )
