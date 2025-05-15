from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Email class representing an email address for an user.
    """

    address: str

    def __repr__(self) -> str:
        return f"Email({self.address!r})"
