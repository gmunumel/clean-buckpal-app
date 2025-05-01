from abc import ABC, abstractmethod
from typing import Dict
from datetime import datetime

from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId


class AbstractActivityRepository(ABC):
    """
    Abstract base class for activity repositories.
    This class defines the interface for activity repositories.
    """

    @abstractmethod
    def get_activities(self) -> Dict[ActivityId, Activity]:
        pass

    @abstractmethod
    def save(self, activity: Activity):
        pass

    @abstractmethod
    def find_by_id(self, activity_id: ActivityId) -> Activity:
        pass

    @abstractmethod
    def find_by_owner_since(
        self, owner_account_id: AccountId, since: datetime
    ) -> list[Activity]:
        pass

    @abstractmethod
    def get_withdrawal_balance_until(
        self, account_id: AccountId, until: datetime
    ) -> float:
        pass

    @abstractmethod
    def get_deposit_balance_until(
        self, account_id: AccountId, until: datetime
    ) -> float:
        pass


class InMemoryDataActivityRepository(AbstractActivityRepository):
    """
    In-memory data repository for activities.
    This class is used for testing purposes and stores activities in memory.
    Attributes:
        activities: A dictionary that maps activity IDs to Activity objects.
    """

    def __init__(self):
        self._activities: Dict[ActivityId, Activity] = {}

    def get_activities(self) -> Dict[ActivityId, Activity]:
        return self._activities

    def save(self, activity: Activity):
        activity_id = activity.get_id()
        if activity_id is None:
            raise ValueError("Activity ID cannot be None.")
        self._activities[activity_id] = activity

    def find_by_id(self, activity_id: ActivityId) -> Activity:
        activity = self._activities.get(activity_id)
        if activity is None:
            raise ValueError(f"Activity with ID {activity_id} not found.")
        return activity

    def find_by_owner_since(
        self, owner_account_id: AccountId, since: datetime
    ) -> list[Activity]:
        return [
            activity
            for activity in self._activities.values()
            if activity.owner_account_id == owner_account_id
            and activity.timestamp >= since
        ]

    def get_withdrawal_balance_until(
        self, account_id: AccountId, until: datetime
    ) -> float:
        return sum(
            activity.money.amount
            for activity in self._activities.values()
            if activity.source_account_id == account_id
            and activity.owner_account_id == account_id
            and activity.timestamp < until
        )

    def get_deposit_balance_until(
        self, account_id: AccountId, until: datetime
    ) -> float:
        return sum(
            activity.money.amount
            for activity in self._activities.values()
            if activity.target_account_id == account_id
            and activity.owner_account_id == account_id
            and activity.timestamp < until
        )
