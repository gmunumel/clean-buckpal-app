from src.adapter.outbound.persistence.in_memory_data_user_repository import (
    InMemoryDataUserRepository,
)
from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.user import User
from src.application.domain.model.status import Status
from src.adapter.outbound.persistence.persistence_model import PersistenceMapper
from src.application.port.outbound.register_user_port import RegisterUserPort
from src.application.port.outbound.list_user_port import ListUserPort


class UserPersistenceAdapter(RegisterUserPort, ListUserPort):
    """
    Persistence adapter for registering a user.
    This adapter interacts with the in-memory data repository to
    register a user in the data source.
    Attributes:
        user_repository: Repository for user data.
    """

    def __init__(self, user_repository: InMemoryDataUserRepository):
        self._user_repository = user_repository

    def register_user(
        self, user_id: UserId, user_name: Name, user_address: Address, status: Status
    ) -> User:
        user = self._user_repository.find_by_id(user_id)
        if user:
            raise ValueError(f"User with ID {user_id} already saved.")

        return self._user_repository.save(
            PersistenceMapper.map_to_user_entity(
                user_id=user_id,
                user_name=user_name,
                address=user_address,
                status=status,
            )
        )

    def list_user(self, user_id: UserId | None) -> list[User] | None:
        if user_id is None:
            dict_users = self._user_repository.get_users()
            return list(dict_users.values())

        user = self._user_repository.find_by_id(user_id)
        return [user] if user else None
