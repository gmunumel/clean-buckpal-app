from abc import ABC, abstractmethod

from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money
from src.application.domain.model.account import Account


class UpdateAccountPort(ABC):
    """
    Port for updating an account.
    This port is used by the application layer to update an account into a data source.
    It provides an interface for updating an account based on the provided account ID and money.
    """

    @abstractmethod
    def update_account(
        self, account_id: AccountId, money: Money
    ) -> Account | dict[str, object]:
        pass
