from abc import ABC, abstractmethod

from src.application.domain.model.activity import Activity
from src.application.port.inbound.list_activity_query import ListActivityQuery


class ListActivityUseCase(ABC):
    """
    Use case for listing activity information.
    This use case is responsible for retrieving activity information
    based on the provided query. It uses the ListActivityQuery
    to specify the criteria for listing activities.
    Attributes:
        list_activity_query: Query for listing activities.
    """

    @abstractmethod
    def list_activity(self, list_activity_query: ListActivityQuery) -> list[Activity]:
        pass
