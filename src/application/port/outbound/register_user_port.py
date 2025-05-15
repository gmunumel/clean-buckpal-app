from abc import ABC, abstractmethod

from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.status import Status
from src.application.domain.model.email import Email
from src.application.domain.model.password import Password


class RegisterUserPort(ABC):
    """
    Port for registering a user.
    This port is used by the application layer to register a user in a data source.
    """

    @abstractmethod
    def register_user(
        self,
        user_id: UserId,
        user_name: Name,
        user_email: Email,
        user_password: Password,
        user_address: Address,
        status: Status,
    ) -> User:
        pass
