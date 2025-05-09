import pytest

from src.application.domain.service.list_account_service import ListAccountService
from src.application.port.inbound.list_account_query import ListAccountQuery
from src.application.domain.model.account_id import AccountId


@pytest.fixture
def list_account_service(mocker):
    list_account_port = mocker.Mock()

    service = ListAccountService(
        list_account_port=list_account_port,
    )
    return service, list_account_port


def test_list_account_service_list_account(list_account_service, given_account_with_id):
    service, list_account_port = list_account_service

    account_id = AccountId(1)
    account = given_account_with_id(account_id)

    list_account_port.list_account.return_value = [account]

    command = ListAccountQuery(account_id=account_id)
    result = service.list_account(command)

    assert result == [account]
    list_account_port.list_account.assert_called_once_with(account_id)
