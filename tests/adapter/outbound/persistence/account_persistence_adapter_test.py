from datetime import datetime
import pytest

from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId
from src.adapter.outbound.persistence.account_persistence_adapter import (
    AccountPersistenceAdapter,
)
from src.adapter.outbound.persistence.in_memory_data_activity_repository import (
    InMemoryDataActivityRepository,
)
from src.adapter.outbound.persistence.in_memory_data_account_repository import (
    InMemoryDataAccountRepository,
)

ACTIVITY_1 = Activity(
    id=ActivityId(1),
    owner_account_id=AccountId(1),
    source_account_id=AccountId(1),
    target_account_id=AccountId(2),
    timestamp=datetime(2018, 8, 8, 8, 0),
    money=Money.of(500),
)
ACTIVITY_2 = Activity(
    id=ActivityId(2),
    owner_account_id=AccountId(2),
    source_account_id=AccountId(1),
    target_account_id=AccountId(2),
    timestamp=datetime(2018, 8, 8, 8, 0),
    money=Money.of(500),
)
ACTIVITY_3 = Activity(
    id=ActivityId(3),
    owner_account_id=AccountId(1),
    source_account_id=AccountId(1),
    target_account_id=AccountId(2),
    timestamp=datetime(2018, 8, 9, 8, 0),
    money=Money.of(1000),
)
ACTIVITY_4 = Activity(
    id=ActivityId(4),
    owner_account_id=AccountId(2),
    source_account_id=AccountId(1),
    target_account_id=AccountId(2),
    timestamp=datetime(2018, 8, 9, 8, 0),
    money=Money.of(1000),
)


@pytest.fixture
def activity_repository():
    return InMemoryDataActivityRepository()


@pytest.fixture
def account_repository():
    return InMemoryDataAccountRepository()


@pytest.fixture
def adapter_under_test(activity_repository, account_repository):
    return AccountPersistenceAdapter(
        activity_repository=activity_repository, account_repository=account_repository
    )


def test_account_persistence_adapter_loads_account(adapter_under_test):
    account_1 = adapter_under_test.insert_account(
        AccountId(1),
        Money.of(0),
        [ACTIVITY_1, ACTIVITY_3],
    )
    account_2 = adapter_under_test.insert_account(
        AccountId(2),
        Money.of(0),
        [ACTIVITY_2, ACTIVITY_4],
    )
    adapter_under_test.update_activities([account_1, account_2])

    account = adapter_under_test.load_account(AccountId(1), datetime(2018, 8, 10, 0, 0))

    assert len(account.activity_window.activities) == 2
    assert account.calculate_balance() == Money.of(-1500)
    adapter_under_test.clean_repositories()
