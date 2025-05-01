from abc import ABC, abstractmethod

from src.application.domain.model.account import Account
from src.application.port.inbound.list_account_query import ListAccountQuery


class ListAccountUseCase(ABC):
    """
    Use case for listing account information.
    This use case is responsible for retrieving account information
    based on the provided query. It uses the ListAccountQuery
    to specify the criteria for listing accounts.
    Attributes:
        list_account_query: Query for listing accounts.
    """

    @abstractmethod
    def list_account(self, list_account_query: ListAccountQuery) -> list[Account]:
        pass
