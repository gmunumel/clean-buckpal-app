from src.application.domain.model.account import Account
from src.application.port.inbound.list_account_query import ListAccountQuery
from src.application.port.inbound.list_account_use_case import ListAccountUseCase
from src.application.port.outbound.list_account_port import ListAccountPort


class ListAccountService(ListAccountUseCase):
    """
    Service for listing account information.
    This service is responsible for retrieving account information
    based on the provided command. It uses the ListAccountPort
    to list accounts from a data source. If no account ID is provided,
    all accounts will be listed.
    Attributes:
        list_account_port: Port for listing accounts.
    """

    def __init__(self, list_account_port: ListAccountPort):
        self._list_acount_port = list_account_port

    def list_account(self, list_account_query: ListAccountQuery) -> list[Account]:
        return self._list_acount_port.list_account(list_account_query.account_id)
