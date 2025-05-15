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
from src.application.port.outbound.list_account_port import ListAccountPort
from src.application.port.outbound.list_activity_port import ListActivityPort
from src.application.port.outbound.update_account_port import UpdateAccountPort
from src.adapter.outbound.persistence.in_memory_data_account_repository import (
    InMemoryDataAccountRepository,
)
from src.adapter.outbound.persistence.in_memory_data_activity_repository import (
    InMemoryDataActivityRepository,
)
from src.adapter.outbound.persistence.persistence_model import PersistenceMapper


class AccountPersistenceAdapter(
    LoadAccountPort,
    ListAccountPort,
    ListActivityPort,
    UpdateAccountPort,
    UpdateAccountStatePort,
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

        return PersistenceMapper.map_to_domain_entity(
            account, activities, withdrawal_balance, deposit_balance
        )

    def update_accounts(self, accounts: list[Account]):
        for account in accounts:
            self._account_repository.update(account)

    def update_activities(self, accounts: list[Account]):
        for account in accounts:
            activity_window = account.activity_window
            for activity in activity_window.activities:
                self._activity_repository.save(activity)

    def list_account(self, account_id: AccountId | None) -> list[Account] | None:
        if account_id is None:
            dict_accounts = self._account_repository.get_accounts()
            return list(dict_accounts.values())

        account = self._account_repository.find_by_id(account_id)
        return [account] if account else None

    def list_activity(self, activity_id: ActivityId | None) -> list[Activity] | None:
        if activity_id is None:
            dict_activities = self._activity_repository.get_activities()
            return list(dict_activities.values())

        activity = self._activity_repository.find_by_id(activity_id)
        return [activity] if activity else None

    def update_account(
        self,
        account_id: AccountId,
        money: Money,
        activities: list[Activity] | None = None,
    ) -> Account | dict[str, object]:
        account = self._account_repository.find_by_id(account_id)
        if account:
            account.baseline_balance = money
            self._account_repository.save(account)
            return {}

        return self._account_repository.save(
            PersistenceMapper.map_to_account_entity(account_id, money, activities or [])
        )

    def clean_repositories(self):
        self._account_repository.clear()
        self._activity_repository.clear()
