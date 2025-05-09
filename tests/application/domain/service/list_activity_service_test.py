import pytest

from src.application.domain.service.list_activity_service import ListActivityService
from src.application.port.inbound.list_activity_query import ListActivityQuery
from src.application.domain.model.activity_id import ActivityId


@pytest.fixture
def list_activity_service(mocker):
    list_activity_port = mocker.Mock()

    service = ListActivityService(
        list_activity_port=list_activity_port,
    )
    return service, list_activity_port


def test_list_activity_service_list_activity(
    list_activity_service, given_activity_with_id
):
    service, list_activity_port = list_activity_service

    activity_id = ActivityId(1)
    activity = given_activity_with_id(activity_id)

    list_activity_port.list_activity.return_value = [activity]

    command = ListActivityQuery(activity_id=activity_id)
    result = service.list_activity(command)

    assert result == [activity]
    list_activity_port.list_activity.assert_called_once_with(activity_id)
