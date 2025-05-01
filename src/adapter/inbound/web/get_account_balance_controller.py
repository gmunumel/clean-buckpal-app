from src.application.port.inbound.get_account_balance_query import (
    GetAccountBalanceQuery,
)
from src.application.port.inbound.get_account_balance_use_case import (
    GetAccountBalanceUseCase,
)
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money


class GetAccountBalanceController:
    def __init__(self, get_account_balance_use_case: GetAccountBalanceUseCase):
        self._get_account_balance_use_case = get_account_balance_use_case

    def get_account_balance(self, account_id: int) -> Money:
        query = GetAccountBalanceQuery(AccountId(account_id))
        return self._get_account_balance_use_case.get_account_balance(query)
