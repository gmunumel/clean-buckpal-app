from abc import ABC, abstractmethod

from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId


class GetActivityPort(ABC):
    """
    Port for listing activities.
    This port is used by the application layer to list activities from a data source.
    It provides an interface for retrieving activities based on the provided activity ID.
    If no activity ID is provided, all activities will be listed.
    """

    @abstractmethod
    def list_activity(self, activity_id: ActivityId | None) -> list[Activity]:
        pass
