from dataclasses import dataclass

from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address


@dataclass(frozen=True)
class RegisterUserCommand:
    """
    RegisterUserCommand class representing a command to manage user accounts.
    """

    user_id: UserId
    user_name: Name
    user_address: Address

    def __post_init__(self):
        pass

    def __repr__(self) -> str:
        return (
            f"RegisterUserCommand(user_id={self.user_id!r}, "
            f"user_name={self.user_name!r}, user_address={self.user_address!r})"
        )
