import pytest

from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.address import Address
from src.application.domain.model.status import Status
from src.application.domain.model.email import Email
from src.application.domain.model.password import Password
from src.adapter.outbound.persistence.user_persistence_adapter import (
    UserPersistenceAdapter,
)
from src.adapter.outbound.persistence.in_memory_data_user_repository import (
    InMemoryDataUserRepository,
)


@pytest.fixture
def user_repository():
    return InMemoryDataUserRepository()


@pytest.fixture
def adapter_under_test(user_repository):
    return UserPersistenceAdapter(user_repository)


def test_user_persistence_adapter_register_user(adapter_under_test):
    user_1 = adapter_under_test.register_user(
        UserId(1),
        Name("foo"),
        Email("foo@example.com"),
        Password("secret"),
        Address(
            street_name="foo",
            street_number=42,
            city="bar",
            postal_code="baz",
            country="qux",
        ),
        Status.enable(),
    )
    users = adapter_under_test.list_user(None)
    user = users[0]
    assert user_1 == user
