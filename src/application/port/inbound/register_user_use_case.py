from abc import ABC, abstractmethod

from src.application.port.inbound.register_user_command import RegisterUserCommand
from src.application.domain.model.user import User


class RegisterUserUseCase(ABC):
    """
    Use case for managing user accounts.
    This use case is responsible for orchestrating the process of managing user
    accounts. It uses the RegisterUserService to perform the actual
    registration and the UserRepository to store and retrieve user data.
    """

    @abstractmethod
    def register_user(self, user_management_command: RegisterUserCommand) -> User:
        pass
