from dataclasses import dataclass


@dataclass(frozen=True)
class Status:
    """
    Status class representing the status.
    """

    is_blocked: bool = False

    @classmethod
    def enable(cls) -> "Status":
        return Status(is_blocked=False)

    @classmethod
    def disable(cls) -> "Status":
        return Status(is_blocked=True)

    def __repr__(self) -> str:
        status = self.is_blocked
        if status:
            return "disable"
        return "enable"
