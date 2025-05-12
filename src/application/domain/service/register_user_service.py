from src.application.domain.model.user import User
from src.application.domain.model.status import Status
from src.application.domain.model.event import UserRegisteredEvent
from src.application.domain.service.event_dispatcher import EventDispatcher
from src.application.port.inbound.register_user_use_case import RegisterUserUseCase
from src.application.port.inbound.register_user_command import RegisterUserCommand
from src.application.port.outbound.register_user_port import RegisterUserPort


class RegisterUserService(RegisterUserUseCase):
    """
    Service for managing user accounts.
    This service is responsible for orchestrating the process of managing user
    accounts. It uses the RegisterUserService to perform the actual
    registration and the UserRepository to store and retrieve user data.
    """

    def __init__(
        self, register_user_port: RegisterUserPort, event_dispatcher: EventDispatcher
    ):
        self._register_user_port = register_user_port
        self._event_dispatcher = event_dispatcher

    def register_user(self, user_management_command: RegisterUserCommand) -> User:
        user = self._register_user_port.register_user(
            user_id=user_management_command.user_id,
            user_name=user_management_command.user_name,
            user_address=user_management_command.user_address,
            status=Status.enable(),
        )

        # Publish an event after user registration
        user_id = user.id
        event = UserRegisteredEvent(user_id=user_id.id)
        self._event_dispatcher.publish(event)

        return user
