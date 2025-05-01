from dataclasses import dataclass


@dataclass(frozen=True)
class AccountId:
    """
    AccountId class representing a unique identifier for an account.
    This class is immutable and provides methods for basic arithmetic operations.
    """

    id: int

    def get_id(self) -> int:
        return self.id

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, AccountId):
            return False
        return self.get_id() == value.get_id()

    def __repr__(self) -> str:
        return f"AccountId({self.id!r})"
