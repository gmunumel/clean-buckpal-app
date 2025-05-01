from src.application.port.inbound.list_account_use_case import ListAccountUseCase
from src.application.port.inbound.list_account_query import ListAccountQuery
from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId


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

    def list_account(self, idd: int | None = None) -> list[Account]:
        account_id = AccountId(idd) if idd is not None else None
        list_account_query = ListAccountQuery(account_id)
        return self._list_account_use_case.list_account(list_account_query)
