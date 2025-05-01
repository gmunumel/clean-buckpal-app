from src.application.domain.model.activity import Activity
from src.application.port.inbound.get_activity_query import GetActivityQuery
from src.application.port.inbound.get_activity_use_case import GetActivityUseCase
from src.application.port.outbound.get_activity_port import GetActivityPort


class GetActivityService(GetActivityUseCase):
    """
    Service for listing activity information.
    This service is responsible for retrieving activity information
    based on the provided command. It uses the GetActivityPort
    to list activities from a data source. If no activity ID is provided,
    all activities will be listed.
    Attributes:
        list_activity_port: Port for listing activities.
    """

    def __init__(self, list_activity_port: GetActivityPort):
        self._list_activity_port = list_activity_port

    def list_activity(self, list_activity_query: GetActivityQuery) -> list[Activity]:
        return self._list_activity_port.list_activity(list_activity_query.get_id())
