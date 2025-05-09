from datetime import datetime, timedelta

import pytest

from src.application.domain.model.activity_window import ActivityWindow
from src.application.domain.model.money import Money
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId
from src.application.domain.model.account_id import AccountId


@pytest.fixture
def activities() -> tuple[Activity, Activity, Activity]:
    activity_start = Activity(
        id=ActivityId(1),
        owner_account_id=AccountId(1),
        source_account_id=AccountId(1),
        target_account_id=AccountId(1),
        timestamp=datetime.now() - timedelta(days=2),
        money=Money.of(0.0),
    )
    activity_middle = Activity(
        id=ActivityId(1),
        owner_account_id=AccountId(1),
        source_account_id=AccountId(1),
        target_account_id=AccountId(1),
        timestamp=datetime.now() - timedelta(days=1),
        money=Money.of(0.0),
    )
    activity_now = Activity(
        id=ActivityId(1),
        owner_account_id=AccountId(1),
        source_account_id=AccountId(1),
        target_account_id=AccountId(1),
        timestamp=datetime.now(),
        money=Money.of(0.0),
    )
    return activity_start, activity_middle, activity_now


def test_activity_window_start_timestamp(activities):
    activity_start, activity_middle, activity_now = activities
    activity_window = ActivityWindow([activity_start, activity_middle, activity_now])

    assert activity_window.get_start_timestamp() == activity_start.timestamp


def test_activity_window_end_timestamp(activities):
    activity_start, activity_middle, activity_now = activities
    activity_window = ActivityWindow([activity_start, activity_middle, activity_now])

    assert activity_window.get_end_timestamp() == activity_now.timestamp


def test_activity_window_calculate_balance():
    account_id_1 = AccountId(1)
    account_id_2 = AccountId(2)

    activity_1 = Activity(
        id=ActivityId(1),
        owner_account_id=account_id_1,
        source_account_id=account_id_1,
        target_account_id=account_id_2,
        timestamp=datetime.now(),
        money=Money.of(999.0),
    )
    activity_2 = Activity(
        id=ActivityId(2),
        owner_account_id=account_id_1,
        source_account_id=account_id_1,
        target_account_id=account_id_2,
        timestamp=datetime.now(),
        money=Money.of(1.0),
    )
    activity_3 = Activity(
        id=ActivityId(2),
        owner_account_id=account_id_1,
        source_account_id=account_id_2,
        target_account_id=account_id_1,
        timestamp=datetime.now(),
        money=Money.of(500.0),
    )

    activity_window = ActivityWindow([activity_1, activity_2, activity_3])

    assert activity_window.calculate_balance(account_id_1) == Money.of(-500.0)
    assert activity_window.calculate_balance(account_id_2) == Money.of(500.0)
