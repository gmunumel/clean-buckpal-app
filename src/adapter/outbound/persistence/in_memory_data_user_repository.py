from abc import ABC, abstractmethod
from typing import Dict

from src.application.domain.model.user import User
from src.application.domain.model.user_id import UserId


class AbstractUserRepository(ABC):
    """
    Abstract base class for user repositories.
    This class defines the interface for user repositories.
    """

    @abstractmethod
    def get_users(self) -> Dict[UserId, User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: UserId) -> User | None:
        pass


class InMemoryDataUserRepository(AbstractUserRepository):
    """
    In-memory data repository for users.
    This class is used for testing purposes and stores users in memory.
    Attributes:
        users: A dictionary that maps user IDs to User objects.
    """

    def __init__(self):
        self._users: Dict[UserId, User] = {}

    def get_users(self) -> Dict[UserId, User]:
        return self._users

    def save(self, user: User) -> User:
        if user.id is None:
            raise ValueError("User ID cannot be None.")
        self._users[user.id] = user
        return user

    def find_by_id(self, user_id: UserId) -> User | None:
        return self._users.get(user_id)

    def clear(self):
        self._users.clear()
