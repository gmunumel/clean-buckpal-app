from src.application.port.inbound.list_account_use_case import ListAccountUseCase
from src.adapter.inbound.web.web_model import (
    WebMapper,
    ListAccountParam,
    AccountResponse,
)


class ListAccountController:
    """
    Controller for listing account information.
    This controller is responsible for handling the request to list
    account information. It uses the ListAccountUseCase to retrieve
    the account information based on the provided query.
    Attributes:
        list_account_use_case: Use case for listing account information.
    """

    def __init__(self, list_account_use_case: ListAccountUseCase):
        self._list_account_use_case = list_account_use_case

    def list_account(
        self, list_account_param: ListAccountParam
    ) -> list[AccountResponse]:
        list_account_query = WebMapper.map_to_list_account_query(list_account_param)
        accounts = self._list_account_use_case.list_account(list_account_query)
        return [WebMapper.map_to_account_entity(account) for account in accounts]
