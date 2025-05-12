from abc import ABC, abstractmethod

from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId


class ListUserPort(ABC):
    """
    Port for listing users.
    This port is used by the application layer to list users from a data source.
    It provides an interface for retrieving users based on the provided user ID.
    If no user ID is provided, all users will be listed.
    The implementation of this port should handle the actual data retrieval
    from the data source, such as a database or an external service.
    """

    @abstractmethod
    def list_user(self, user_id: UserId | None) -> list[User] | None:
        pass
