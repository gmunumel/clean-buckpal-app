from abc import ABC, abstractmethod
from datetime import datetime

from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId


class LoadAccountPort(ABC):
    """
    Port for loading an account.
    This port is used by the application layer to load an account from a data source.
    """

    @abstractmethod
    def load_account(self, account_id: AccountId, baseline_date: datetime) -> Account:

        pass