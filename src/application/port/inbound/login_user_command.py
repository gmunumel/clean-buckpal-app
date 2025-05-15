from dataclasses import dataclass
from email.utils import parseaddr

from src.application.domain.model.email import Email
from src.application.domain.model.password import Password


@dataclass(frozen=True)
class LoginUserCommand:
    """
    LoginUserCommand class representing a command to log in a user.
    """

    email: Email
    password: Password

    def __post_init__(self):
        if not self.email:
            raise ValueError("Email must be provided.")
        if not self._is_valid_email():
            raise ValueError("Invalid email format.")
        if not self.password:
            raise ValueError("Password must be provided.")

    def _is_valid_email(self) -> bool:
        return "@" in parseaddr(self.email.address)[1]

    def __repr__(self) -> str:
        return f"LoginUserCommand(email={self.email!r})"
