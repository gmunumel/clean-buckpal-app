from src.application.port.inbound.get_account_balance_use_case import (
    GetAccountBalanceUseCase,
)
from src.adapter.inbound.web.web_model import (
    WebMapper,
    GetAccountBalanceParam,
    GetAccountBalanceResponse,
)


class GetAccountBalanceController:
    """
    Controller for getting the account balance.
    This controller is responsible for handling the request to get
    the account balance. It uses the GetAccountBalanceUseCase to
    retrieve the account balance based on the provided query.
    Attributes:
        get_account_balance_use_case: Use case for getting the account balance.
    """

    def __init__(self, get_account_balance_use_case: GetAccountBalanceUseCase):
        self._get_account_balance_use_case = get_account_balance_use_case

    def get_account_balance(
        self, get_account_balance_param: GetAccountBalanceParam
    ) -> GetAccountBalanceResponse:
        query = WebMapper.map_to_get_account_balance_query(get_account_balance_param)
        account_balance = self._get_account_balance_use_case.get_account_balance(query)
        return WebMapper.map_to_get_account_balance_entity(
            get_account_balance_param.account_id, account_balance
        )
