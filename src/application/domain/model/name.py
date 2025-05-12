from dataclasses import dataclass


@dataclass(frozen=True)
class Name:
    """
    Name class representing a name for an user.
    """

    full_name: str

    def __repr__(self) -> str:
        return f"Name({self.full_name!r})"
