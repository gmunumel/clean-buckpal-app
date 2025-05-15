from typing import Set

from src.application.port.outbound.account_lock import AccountLock
from src.application.domain.model.account_id import AccountId


class InMemoryAccountLock(AccountLock):
    """
    A simple in-memory implementation of AccountLock for testing purposes.
    """

    def __init__(self):
        self._locked_accounts: Set[AccountId] = set()

    def lock_account(self, account_id: AccountId):
        if account_id in self._locked_accounts:
            raise ValueError(f"Account {account_id} is already locked.")
        self._locked_accounts.add(account_id)

    def release_account(self, account_id: AccountId):
        self._locked_accounts.remove(account_id)
