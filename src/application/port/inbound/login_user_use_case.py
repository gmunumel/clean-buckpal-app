from abc import ABC, abstractmethod

from src.application.port.inbound.login_user_command import LoginUserCommand
from src.application.domain.model.user import User


class LoginUserUseCase(ABC):
    """
    Use case for managing user accounts.
    This use case is responsible for orchestrating the process of managing user
    accounts. It uses the LoginUserService to perform the actual
    login and the UserRepository to store and retrieve user data.
    """

    @abstractmethod
    def login_user(self, user_management_command: LoginUserCommand) -> User:
        pass
