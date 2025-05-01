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
    def save(self, account: Account):
        pass

    @abstractmethod
    def find_by_id(self, account_id: AccountId) -> Account:
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

    def save(self, account: Account):
        if account.get_id() is None:
            raise ValueError("Account ID cannot be None.")
        self._accounts[account.get_id()] = account

    def find_by_id(self, account_id: AccountId) -> Account:
        account = self._accounts.get(account_id)
        if account is None:
            raise ValueError(f"Account with ID {account_id} not found.")
        return account
