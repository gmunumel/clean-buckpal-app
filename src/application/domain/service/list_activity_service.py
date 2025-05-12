from src.application.domain.model.activity import Activity
from src.application.domain.service.validation_exception import ValidationException
from src.application.port.inbound.list_activity_query import ListActivityQuery
from src.application.port.inbound.list_activity_use_case import ListActivityUseCase
from src.application.port.outbound.list_activity_port import ListActivityPort


class ListActivityService(ListActivityUseCase):
    """
    Service for listing activity information.
    This service is responsible for retrieving activity information
    based on the provided command. It uses the ListActivityPort
    to list activities from a data source. If no activity ID is provided,
    all activities will be listed.
    Attributes:
        list_activity_port: Port for listing activities.
    """

    def __init__(self, list_activity_port: ListActivityPort):
        self._list_activity_port = list_activity_port

    def list_activity(self, list_activity_query: ListActivityQuery) -> list[Activity]:
        activities = self._list_activity_port.list_activity(
            list_activity_query.activity_id
        )
        if activities is None:
            raise ValidationException(404, "Activity not found")
        return activities
