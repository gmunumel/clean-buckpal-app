from dataclasses import dataclass

from src.application.domain.model.activity_id import ActivityId


@dataclass(frozen=True)
class ListActivityQuery:
    """
    ListActivityQuery class representing a query to list activities.
    """

    activity_id: ActivityId | None = None

    def __repr__(self) -> str:
        return f"ListActivityQuery(activity_id={self.activity_id!r})"
