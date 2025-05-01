from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.application.domain.model.money import Money
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity_window import ActivityWindow
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId


@dataclass()
class Account:
    id: AccountId
    #  This was the balance of the account before the first
    # activity in the activity_window.
    baseline_balance: Money
    activity_window: ActivityWindow

    @classmethod
    def without_id(
        cls, baseline_balance: Money, activity_window: ActivityWindow
    ) -> "Account":
        return Account(
            id=AccountId(0),
            baseline_balance=baseline_balance,
            activity_window=activity_window,
        )

    @classmethod
    def with_id(
        cls,
        account_id: AccountId,
        baseline_balance: Money,
        activity_window: ActivityWindow,
    ) -> "Account":
        return Account(
            id=account_id,
            baseline_balance=baseline_balance,
            activity_window=activity_window,
        )

    def get_id(self) -> AccountId:
        return self.id

    def get_activity_window(self) -> ActivityWindow:
        return self.activity_window

    def get_baseline_balance(self) -> Money:
        return self.baseline_balance

    def calculate_balance(self) -> Money:
        return Money.add(
            self.baseline_balance, self.activity_window.calculate_balance(self.get_id())
        )

    def withdraw(self, money: Money, target_account_id: AccountId) -> bool:
        if not self.may_withdraw(money):
            return False

        withdrawal = Activity(
            id=ActivityId(uuid4().int),
            owner_account_id=self.get_id(),
            source_account_id=self.get_id(),
            target_account_id=target_account_id,
            timestamp=datetime.now(),
            money=money,
        )
        self.activity_window.add_activity(withdrawal)
        return True

    def may_withdraw(self, money: Money) -> bool:
        return Money.add(self.calculate_balance(), money.negate()).is_positive_or_zero()

    def deposit(self, money: Money, source_account_id: AccountId):
        deposit = Activity(
            id=ActivityId(uuid4().int),
            owner_account_id=self.get_id(),
            source_account_id=source_account_id,
            target_account_id=self.get_id(),
            timestamp=datetime.now(),
            money=money,
        )
        self.activity_window.add_activity(deposit)

    def __repr__(self) -> str:
        return (
            f"Account(id={self.id!r}, "
            f"baseline_balance={self.baseline_balance!r}, "
            f"activity_window={self.activity_window!r})"
        )
