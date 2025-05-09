from src.application.port.inbound.list_activity_use_case import ListActivityUseCase
from src.adapter.inbound.web.web_model import (
    WebMapper,
    ListActivityParam,
    ActivityResponse,
)


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

    def list_activity(
        self, list_activity_param: ListActivityParam
    ) -> list[ActivityResponse]:
        list_activity_query = WebMapper.map_to_list_activity_query(list_activity_param)
        activities = self._list_activity_use_case.list_activity(list_activity_query)
        return [WebMapper.map_to_activity_entity(activity) for activity in activities]
