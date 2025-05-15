from src.application.port.inbound.login_user_use_case import LoginUserUseCase
from src.adapter.inbound.web.web_model import (
    WebMapper,
    LoginUserRequest,
    LoginUserResponse,
)
from src.common.jwt_utils import create_jwt_token


class LoginUserController:
    """
    Controller for logging in a user.
    This controller handles the HTTP request for logging in a user and
    delegates the request to the LoginUserUseCase.
    It provides a method to log in a user based on the provided LoginUserRequest.
    Attributes:
        login_user_use_case: Use case for logging in a user.
    """

    def __init__(self, login_user_use_case: LoginUserUseCase):
        self._login_user_use_case = login_user_use_case

    def login_user(self, login_user_request: LoginUserRequest) -> LoginUserResponse:
        user_management_command = WebMapper.map_to_login_user_command(
            login_user_request
        )
        user = self._login_user_use_case.login_user(user_management_command)
        token = create_jwt_token(user)
        return WebMapper.map_to_login_user_entity(token)
