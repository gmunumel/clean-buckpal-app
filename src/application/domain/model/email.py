import re

from dataclasses import dataclass

EMAIL_REGEX = r"^(?!.*\.\.)[\w\.-]+@([\w-]+\.)+[a-zA-Z]{2,}$"


@dataclass(frozen=True)
class Email:
    """
    Email class representing an email address for an user.
    """

    address: str

    def __post_init__(self):
        if not self._is_valid_email():
            raise ValueError("Invalid email address.")

    def _is_valid_email(self) -> bool:
        if not re.match(EMAIL_REGEX, self.address):
            raise ValueError(f"Invalid email address: {self.address}")
        return True

    def __repr__(self) -> str:
        return f"{self.address}"
