from abc import ABC, abstractmethod

from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money
from src.application.domain.model.account import Account


class InsertAccountPort(ABC):
    """
    Port for inserting an account.
    This port is used by the application layer to insert an account into a data source.
    It provides an interface for inserting an account based on the provided account ID and money.
    """

    @abstractmethod
    def insert_account(self, account_id: AccountId, money: Money) -> Account:
        pass
