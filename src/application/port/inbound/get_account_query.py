from dataclasses import dataclass

from src.application.domain.model.account_id import AccountId


@dataclass(frozen=True)
class GetAccountQuery:
    """
    GetAccountQuery class representing a query to list accounts.
    """

    id: AccountId | None = None

    def get_id(self) -> AccountId | None:
        return self.id

    def __repr__(self) -> str:
        return f"GetAccountQuery(id={self.id!r})"
