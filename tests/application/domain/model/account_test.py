from datetime import datetime

import pytest

from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId
from src.application.domain.model.money import Money
from src.application.domain.model.activity_window import ActivityWindow


@pytest.fixture
def account() -> Account:
    account_id = AccountId(42)
    return Account.with_id(
        account_id,
        Money.of(100.0),
        ActivityWindow(
            [
                Activity(
                    id=ActivityId(1),
                    owner_account_id=AccountId(1),
                    source_account_id=AccountId(2),
                    target_account_id=account_id,
                    timestamp=datetime.now(),
                    money=Money.of(50.0),
                ),
                Activity(
                    id=ActivityId(2),
                    owner_account_id=AccountId(1),
                    source_account_id=AccountId(2),
                    target_account_id=account_id,
                    timestamp=datetime.now(),
                    money=Money.of(1.0),
                ),
            ]
        ),
    )


def test_account_balance(account):
    balance = account.calculate_balance()
    assert balance == Money.of(151.0)


def test_account_withdrawal(account):
    success = account.withdraw(Money.of(100.0), AccountId(43))

    assert success
    assert len(account.activity_window.activities) == 3
    assert account.calculate_balance() == Money.of(51.0)


def test_account_withdrawal_exceeds_balance(account):
    success = account.withdraw(Money.of(152.0), AccountId(43))

    assert not success
    assert len(account.activity_window.activities) == 2
    assert account.calculate_balance() == Money.of(151.0)


def test_account_deposit(account):
    success = account.deposit(Money.of(49.0), AccountId(43))

    assert success
    assert len(account.activity_window.activities) == 3
    assert account.calculate_balance() == Money.of(200.0)
