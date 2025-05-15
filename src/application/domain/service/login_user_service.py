from src.application.domain.model.user import User
from src.application.domain.model.password import Password
from src.application.port.inbound.login_user_use_case import LoginUserUseCase
from src.application.port.inbound.login_user_command import LoginUserCommand
from src.application.port.outbound.login_user_port import LoginUserPort
from src.application.domain.service.validation_exception import ValidationException


class LoginUserService(LoginUserUseCase):
    """
    Service for managing user accounts.
    This service is responsible for orchestrating the process of managing user
    accounts. It uses the LoginUserService to perform the actual
    login and the UserRepository to store and retrieve user data.
    """

    def __init__(self, login_user_port: LoginUserPort):
        self._login_user_port = login_user_port

    def login_user(self, user_management_command: LoginUserCommand) -> User:
        user_in_db = self._login_user_port.login_user(user_management_command.email)

        if not user_in_db:
            raise ValidationException(404, "User email not found.")

        password = user_management_command.password
        password_hash = Password(hashed=str(user_in_db.password))
        if not password_hash.verify(str(password)):
            raise ValidationException(401, "Invalid password.")

        return user_in_db
