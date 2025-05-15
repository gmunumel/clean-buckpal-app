from abc import ABC, abstractmethod
from typing import Dict

from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId


class AbstractAccountRepository(ABC):
    """
    Abstract base class for account repositories.
    This class defines the interface for account repositories.
    """

    @abstractmethod
    def get_accounts(self) -> Dict[AccountId, Account]:
        pass

    @abstractmethod
    def save(self, account: Account) -> Account:
        pass

    @abstractmethod
    def find_by_id(self, account_id: AccountId) -> Account | None:
        pass


class InMemoryDataAccountRepository(AbstractAccountRepository):
    """
    In-memory data repository for accounts.
    This class is used for testing purposes and stores accounts in memory.
    Attributes:
        accounts: A dictionary that maps account IDs to Account objects.
    """

    def __init__(self):
        self._accounts: Dict[AccountId, Account] = {}

    def get_accounts(self) -> Dict[AccountId, Account]:
        return self._accounts

    def save(self, account: Account) -> Account:
        self._accounts[account.id] = account
        return account

    def update(self, account: Account) -> Account:
        activity_window = self._accounts[account.id].activity_window
        new_activity_window = account.activity_window
        activity_window.activities.append(new_activity_window.activities[0])
        return self._accounts[account.id]

    def find_by_id(self, account_id: AccountId) -> Account | None:
        return self._accounts.get(account_id)

    def clear(self):
        self._accounts.clear()
