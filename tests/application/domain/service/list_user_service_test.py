import pytest

from src.application.domain.service.list_user_service import ListUserService
from src.application.port.inbound.list_user_query import ListUserQuery
from src.application.domain.model.user_id import UserId


@pytest.fixture
def list_user_service(mocker):
    list_user_port = mocker.Mock()

    service = ListUserService(
        list_user_port=list_user_port,
    )
    return service, list_user_port


def test_list_user_service_list_user(list_user_service, given_user_with_id):
    service, list_user_port = list_user_service

    user_id = UserId(1)
    user = given_user_with_id(user_id)

    list_user_port.list_user.return_value = [user]

    command = ListUserQuery(user_id=user_id)
    result = service.list_user(command)

    assert result == [user]
    list_user_port.list_user.assert_called_once_with(user_id)
