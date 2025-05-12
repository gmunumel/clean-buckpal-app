from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    """
    UserId class representing a unique identifier for an user.
    """

    id: int

    def __repr__(self) -> str:
        return f"UserId({self.id!r})"
