from src.application.port.inbound.list_activity_use_case import ListActivityUseCase
from src.application.port.inbound.list_activity_query import ListActivityQuery
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId


class ListActivityController:
    """
    Controller for listing activity information.
    This controller is responsible for handling the request to list
    activity information. It uses the ListActivityUseCase to retrieve
    the activity information based on the provided query.
    Attributes:
        list_activity_use_case: Use case for listing activity information.
    """

    def __init__(self, list_activity_use_case: ListActivityUseCase):
        self._list_activity_use_case = list_activity_use_case

    def list_activity(self, idd: int | None = None) -> list[Activity]:
        activity_id = ActivityId(idd) if idd is not None else None
        list_activity_query = ListActivityQuery(activity_id)
        return self._list_activity_use_case.list_activity(list_activity_query)
