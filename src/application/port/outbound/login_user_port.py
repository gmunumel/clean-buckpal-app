from abc import ABC, abstractmethod

from src.application.domain.model.user import User
from src.application.domain.model.email import Email


class LoginUserPort(ABC):
    """
    Port for logging in a user.
    This port is used by the application layer to log in a user in a data source.
    """

    @abstractmethod
    def login_user(self, email: Email) -> User | None:
        pass
