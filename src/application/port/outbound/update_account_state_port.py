from abc import ABC, abstractmethod

from src.application.domain.model.account import Account


class UpdateAccountStatePort(ABC):
    """
    Port for updating the state of an account.
    This port is used by the application layer to update the state of an account
    after a transaction.
    """

    @abstractmethod
    def update_activities(self, account: Account):
        pass
