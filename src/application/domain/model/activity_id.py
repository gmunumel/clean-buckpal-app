from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityId:
    """
    ActivityId class representing a unique identifier for an activity.
    """

    id: int

    def __repr__(self) -> str:
        return f"ActivityId({self.id!r})"
