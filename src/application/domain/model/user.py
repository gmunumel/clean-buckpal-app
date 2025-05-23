from dataclasses import dataclass

from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.status import Status
from src.application.domain.model.email import Email
from src.application.domain.model.password import Password


@dataclass(frozen=True)
class User:
    """
    User class representing an user in the system.
    This class is immutable and provides methods for basic user operations.
    """

    id: UserId
    name: Name
    address: Address
    status: Status
    email: Email
    password: Password

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, name={self.name!r}, "
            f"address={self.address!r}, Status={self.status!r}, "
            f"email={self.email!r})"
        )
