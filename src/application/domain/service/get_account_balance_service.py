from datetime import datetime

from src.application.port.inbound.get_account_balance_use_case import (
    GetAccountBalanceUseCase,
)
from src.application.port.outbound.load_account_port import LoadAccountPort
from src.application.port.inbound.get_account_balance_query import (
    GetAccountBalanceQuery,
)
from src.application.domain.model.money import Money


class GetAccountBalanceService(GetAccountBalanceUseCase):
    """
    Service for retrieving the balance of an account.
    This service is responsible for retrieving the balance of an account
    based on the provided query. It uses the LoadAccountPort
    to load account information from a data source.
    Attributes:
        load_account_port: Port for loading account information.
    """

    def __init__(self, load_account_port: LoadAccountPort):
        self._load_account_port = load_account_port

    def get_account_balance(self, query: GetAccountBalanceQuery) -> Money:
        account_loaded = self._load_account_port.load_account(
            query.account_id, datetime.now()
        )
        return account_loaded.calculate_balance()
