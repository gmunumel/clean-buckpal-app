from dataclasses import dataclass


@dataclass(frozen=True)
class ActivityId:
    """
    ActivityId class representing a unique identifier for an activity.
    """

    id: int

    def get_id(self) -> int:
        return self.id

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ActivityId):
            return False
        return self.get_id() == value.get_id()

    def __repr__(self) -> str:
        return f"ActivityId({self.id!r})"
