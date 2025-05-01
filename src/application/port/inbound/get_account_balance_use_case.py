from abc import ABC, abstractmethod

from src.application.domain.model.money import Money
from src.application.port.inbound.get_account_balance_query import (
    GetAccountBalanceQuery,
)


class GetAccountBalanceUseCase(ABC):
    """
    Use case for retrieving the balance of an account.
    This use case is responsible for retrieving the balance of an account
    based on the provided query. It uses the GetAccountBalanceQuery
    to specify the criteria for retrieving the account balance.
    Attributes:
        get_account_balance_query: Query for retrieving account balance.
    """

    @abstractmethod
    def get_account_balance(self, query: GetAccountBalanceQuery) -> Money:
        pass
