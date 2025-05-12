from src.application.domain.model.user import User
from src.application.domain.service.validation_exception import ValidationException
from src.application.port.inbound.list_user_query import ListUserQuery
from src.application.port.inbound.list_user_use_case import ListUserUseCase
from src.application.port.outbound.list_user_port import ListUserPort


class ListUserService(ListUserUseCase):
    """
    Service for listing user information.
    This service is responsible for retrieving user information
    based on the provided command. It uses the ListUserPort
    to list users from a data source. If no user ID is provided,
    all users will be listed.
    Attributes:
        list_user_port: Port for listing users.
    """

    def __init__(self, list_user_port: ListUserPort):
        self._list_acount_port = list_user_port

    def list_user(self, list_user_query: ListUserQuery) -> list[User]:
        users = self._list_acount_port.list_user(list_user_query.user_id)
        if users is None:
            raise ValidationException(404, "User not found")
        return users
