from dataclasses import dataclass

from src.application.domain.model.activity_id import ActivityId


@dataclass(frozen=True)
class GetActivityQuery:
    """
    GetActivityQuery class representing a query to list activities.
    """

    id: ActivityId | None = None

    def get_id(self) -> ActivityId | None:
        return self.id

    def __repr__(self) -> str:
        return f"GetActivityQuery(id={self.id!r})"
