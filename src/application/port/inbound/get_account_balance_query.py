from dataclasses import dataclass

from src.application.domain.model.account_id import AccountId


@dataclass(frozen=True)
class GetAccountBalanceQuery:
    """
    GetAccountBalanceQuery class representing a query to get the balance of an account.
    """

    account_id: AccountId

    def __repr__(self) -> str:
        return f"GetAccountBalanceQuery(id={self.account_id!r})"
