from dataclasses import dataclass

from src.application.domain.model.account_id import AccountId


@dataclass(frozen=True)
class ListAccountQuery:
    """
    ListAccountQuery class representing a query to list accounts.
    """

    account_id: AccountId | None = None

    def __repr__(self) -> str:
        return f"ListAccountQuery(account_id={self.account_id!r})"
