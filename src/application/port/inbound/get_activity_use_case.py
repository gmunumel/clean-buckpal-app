from abc import ABC, abstractmethod

from src.application.domain.model.activity import Activity
from src.application.port.inbound.get_activity_query import GetActivityQuery


class GetActivityUseCase(ABC):
    """
    Use case for listing activity information.
    This use case is responsible for retrieving activity information
    based on the provided query. It uses the GetActivityQuery
    to specify the criteria for listing activities.
    Attributes:
        list_activity_query: Query for listing activities.
    """

    @abstractmethod
    def list_activity(self, list_activity_query: GetActivityQuery) -> list[Activity]:
        pass
