from src.application.port.inbound.get_activity_use_case import GetActivityUseCase
from src.application.port.inbound.get_activity_query import GetActivityQuery
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId


class GetActivityController:
    """
    Controller for listing activity information.
    This controller is responsible for handling the request to list
    activity information. It uses the GetActivityUseCase to retrieve
    the activity information based on the provided query.
    Attributes:
        list_activity_use_case: Use case for listing activity information.
    """

    def __init__(self, list_activity_use_case: GetActivityUseCase):
        self._list_activity_use_case = list_activity_use_case

    def list_activity(self, idd: int | None = None) -> list[Activity]:
        activity_id = ActivityId(idd) if idd is not None else None
        list_activity_query = GetActivityQuery(activity_id)
        return self._list_activity_use_case.list_activity(list_activity_query)
