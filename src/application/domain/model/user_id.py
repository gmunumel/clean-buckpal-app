from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    """
    UserId class representing a unique identifier for an user.
    """

    id: int

    def __post_init__(self):
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("UserId must be a positive integer.")

    def __repr__(self) -> str:
        return f"{self.id!r}"
