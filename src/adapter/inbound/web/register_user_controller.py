from src.application.port.inbound.register_user_use_case import RegisterUserUseCase


from src.adapter.inbound.web.web_model import (
    WebMapper,
    RegisterUserRequest,
    RegisterUserResponse,
)


class RegisterUserController:
    """
    Controller for registering a new user.
    This controller is responsible for handling the request to create
    a new user. It uses the RegisterUserUseCase to perform the
    registration of the user based on the provided command.
    Attributes:
        register_user_use_case: Use case for registering a new user.
    """

    def __init__(self, register_user_use_case: RegisterUserUseCase):
        self._register_user_use_case = register_user_use_case

    def register_user(
        self, register_user_request: RegisterUserRequest
    ) -> RegisterUserResponse:
        user_management_command = WebMapper.map_to_register_user_command(
            register_user_request
        )
        user = self._register_user_use_case.register_user(user_management_command)
        return WebMapper.map_to_register_user_entity(user)
