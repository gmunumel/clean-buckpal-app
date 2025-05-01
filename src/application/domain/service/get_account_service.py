from src.application.domain.model.account import Account
from src.application.port.inbound.get_account_query import GetAccountQuery
from src.application.port.inbound.get_account_use_case import GetAccountUseCase
from src.application.port.outbound.get_account_port import GetAccountPort


class GetAccountService(GetAccountUseCase):
    """
    Service for listing account information.
    This service is responsible for retrieving account information
    based on the provided command. It uses the GetAccountPort
    to list accounts from a data source. If no account ID is provided,
    all accounts will be listed.
    Attributes:
        list_account_port: Port for listing accounts.
    """

    def __init__(self, list_account_port: GetAccountPort):
        self._list_acount_port = list_account_port

    def list_account(self, list_account_query: GetAccountQuery) -> list[Account]:
        return self._list_acount_port.list_account(list_account_query.get_id())
