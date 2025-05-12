from dataclasses import dataclass

from src.application.domain.model.user_id import UserId


@dataclass(frozen=True)
class ListUserQuery:
    """
    ListUserQuery class representing a query to list users.
    """

    user_id: UserId | None = None

    def __repr__(self) -> str:
        return f"ListUserQuery(user_id={self.user_id!r})"
