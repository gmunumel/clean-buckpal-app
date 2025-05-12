from abc import ABC, abstractmethod

from src.application.domain.model.user import User
from src.application.port.inbound.list_user_query import ListUserQuery


class ListUserUseCase(ABC):
    """
    Use case for listing user information.
    This use case is responsible for retrieving user information
    based on the provided query. It uses the ListUserQuery
    to specify the criteria for listing users.
    Attributes:
        list_user_query: Query for listing users.
    """

    @abstractmethod
    def list_user(self, list_user_query: ListUserQuery) -> list[User]:
        pass
