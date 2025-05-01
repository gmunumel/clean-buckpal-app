from abc import ABC, abstractmethod

from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId


class ListAccountPort(ABC):
    """
    Port for listing accounts.
    This port is used by the application layer to list accounts from a data source.
    It provides an interface for retrieving accounts based on the provided account ID.
    If no account ID is provided, all accounts will be listed.
    """

    @abstractmethod
    def list_account(self, account_id: AccountId | None) -> list[Account]:
        pass
