from dataclasses import dataclass


@dataclass(frozen=True)
class AccountId:
    """
    AccountId class representing a unique identifier for an account.
    This class is immutable and provides methods for basic arithmetic operations.
    """

    id: int

    def __repr__(self) -> str:
        return f"AccountId({self.id!r})"
