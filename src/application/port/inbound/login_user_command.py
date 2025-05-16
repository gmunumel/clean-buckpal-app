from dataclasses import dataclass

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
        if not self.password:
            raise ValueError("Password must be provided.")

    def __repr__(self) -> str:
        return f"LoginUserCommand(email={self.email!r})"
