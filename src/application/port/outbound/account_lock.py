from abc import ABC, abstractmethod

from src.application.domain.model.account_id import AccountId


class AccountLock(ABC):
    """
    Port for locking and unlocking accounts.
    This port is used by the application layer to lock and unlock accounts
    during a transaction.
    """

    @abstractmethod
    def lock_account(self, account_id: AccountId):
        pass

    @abstractmethod
    def release_account(self, account_id: AccountId):
        pass
