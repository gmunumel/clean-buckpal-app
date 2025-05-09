import pytest

from src.application.port.inbound.insert_account_command import InsertAccountCommand
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money


def test_insert_account_command():
    account_id = AccountId(1)
    money = Money.of(100.0)

    command = InsertAccountCommand(account_id=account_id, money=money)

    assert command.account_id == account_id
    assert command.money == money


def test_insert_account_command_money_validation_fails():
    account_id = AccountId(1)
    money = None

    with pytest.raises(ValueError, match="Money must be provided."):
        InsertAccountCommand(account_id=account_id, money=money)  # type: ignore


def test_insert_account_command_money_validation_bigger_than_zero():
    account_id = AccountId(1)
    money = Money.of(-10)

    with pytest.raises(ValueError, match="Money must be greater than zero."):
        InsertAccountCommand(account_id=account_id, money=money)


def test_insert_account_command_account_id_validation_fails():
    account_id = None
    money = Money.of(-10)

    with pytest.raises(ValueError, match="Account ID must be provided."):
        InsertAccountCommand(account_id=account_id, money=money)  # type: ignore
