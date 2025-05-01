from dataclasses import dataclass

from src.application.domain.model.activity_id import ActivityId


@dataclass(frozen=True)
class ListActivityQuery:
    """
    ListActivityQuery class representing a query to list activities.
    """

    id: ActivityId | None = None

    def get_id(self) -> ActivityId | None:
        return self.id

    def __repr__(self) -> str:
        return f"ListActivityQuery(id={self.id!r})"
