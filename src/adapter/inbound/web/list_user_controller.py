from src.application.port.inbound.list_user_use_case import ListUserUseCase
from src.adapter.inbound.web.web_model import (
    WebMapper,
    ListUserParam,
    UserResponse,
)


class ListUserController:
    """
    Controller for listing user information.
    This controller is responsible for handling the request to list
    user information. It uses the ListUserUseCase to retrieve
    the user information based on the provided query.
    Attributes:
        list_user_use_case: Use case for listing user information.
    """

    def __init__(self, list_user_use_case: ListUserUseCase):
        self._list_user_use_case = list_user_use_case

    def list_user(self, list_user_param: ListUserParam) -> list[UserResponse]:
        list_user_query = WebMapper.map_to_list_user_query(list_user_param)
        users = self._list_user_use_case.list_user(list_user_query)
        return [WebMapper.map_to_user_entity(user) for user in users]
