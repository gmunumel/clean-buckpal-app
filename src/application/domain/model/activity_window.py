from dataclasses import dataclass
from datetime import datetime

from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money
from src.application.domain.model.activity import Activity


@dataclass
class ActivityWindow:
    """
    ActivityWindow class representing a collection of financial activities.
    This class provides methods to manage and analyze the activities within the window.
    """

    activities: list[Activity]

    def add_activity(self, activity: Activity):
        self.activities.append(activity)

    def get_start_timestamp(self) -> datetime:
        return min(activity.timestamp for activity in self.activities)

    def get_end_timestamp(self) -> datetime:
        return max(activity.timestamp for activity in self.activities)

    def calculate_balance(self, account_id: AccountId) -> Money:
        deposit_balance = self._calculate_deposit_balance(account_id)
        withdraw_balance = self._calculate_withdraw_balance(account_id)
        return Money.add(deposit_balance, withdraw_balance.negate())

    def _calculate_deposit_balance(self, account_id: AccountId) -> Money:
        deposit_balance = Money.zero()
        for activity in self.activities:
            if activity.target_account_id == account_id:
                deposit_balance = Money.add(deposit_balance, activity.money)
        return deposit_balance

    def _calculate_withdraw_balance(self, account_id: AccountId) -> Money:
        withdraw_balance = Money.zero()
        for activity in self.activities:
            if activity.source_account_id == account_id:
                withdraw_balance = Money.add(withdraw_balance, activity.money)
        return withdraw_balance

    def __repr__(self) -> str:
        return f"ActivityWindow(activities={self.activities!r})"
