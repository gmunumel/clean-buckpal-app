from datetime import datetime

from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId
from src.application.domain.model.money import Money
from src.application.port.outbound.update_account_state_port import (
    UpdateAccountStatePort,
)
from src.application.port.outbound.load_account_port import LoadAccountPort
from src.application.port.outbound.get_account_port import GetAccountPort
from src.application.port.outbound.get_activity_port import GetActivityPort
from src.adapter.outbound.persistence.in_memory_data_account_repository import (
    InMemoryDataAccountRepository,
)
from src.adapter.outbound.persistence.in_memory_data_activity_repository import (
    InMemoryDataActivityRepository,
)
from src.application.domain.model.activity_window import ActivityWindow


class AccountPersistenceAdapter(
    LoadAccountPort, GetAccountPort, GetActivityPort, UpdateAccountStatePort
):
    """
    Persistence adapter for loading and updating account/activity information.
    This adapter interacts with the in-memory data repositories to
    load account information, update activities, and list accounts and activities.
    Attributes:
        account_repository: Repository for account data.
        activity_repository: Repository for activity data.
    """

    def __init__(
        self,
        account_repository: InMemoryDataAccountRepository,
        activity_repository: InMemoryDataActivityRepository,
    ):
        self._account_repository = account_repository
        self._activity_repository = activity_repository

    def load_account(self, account_id: AccountId, baseline_date: datetime) -> Account:
        account = self._account_repository.find_by_id(account_id)
        if not account:
            raise ValueError(f"Account with ID {account_id} not found.")

        activities = self._activity_repository.find_by_owner_since(
            account_id, baseline_date
        )

        withdrawal_balance = self._activity_repository.get_withdrawal_balance_until(
            account_id, baseline_date
        )

        deposit_balance = self._activity_repository.get_deposit_balance_until(
            account_id, baseline_date
        )

        baseline_balance = Money.subtract(
            Money.of(deposit_balance), Money.of(withdrawal_balance)
        )

        account_id = account.get_id()
        return Account.with_id(
            AccountId(account_id.get_id()), baseline_balance, ActivityWindow(activities)
        )

    def update_activities(self, account: Account):
        for activity in account.get_activity_window().get_activities():
            if activity.get_id() is None:
                self._activity_repository.save(activity)

    def list_account(self, account_id: AccountId | None) -> list[Account]:
        if account_id is None:
            dict_accounts = self._account_repository.get_accounts()
            return list(dict_accounts.values())

        account = self._account_repository.find_by_id(account_id)
        return [account] if account else []

    def list_activity(self, activity_id: ActivityId | None) -> list[Activity]:
        if activity_id is None:
            dict_activities = self._activity_repository.get_activities()
            return list(dict_activities.values())

        activity = self._activity_repository.find_by_id(activity_id)
        return [activity] if activity else []
