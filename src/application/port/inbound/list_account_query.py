from dataclasses import dataclass

from src.application.domain.model.account_id import AccountId


@dataclass(frozen=True)
class ListAccountQuery:
    """
    ListAccountQuery class representing a query to list accounts.
    """

    id: AccountId | None = None

    def get_id(self) -> AccountId | None:
        return self.id

    def __repr__(self) -> str:
        return f"ListAccountQuery(id={self.id!r})"
