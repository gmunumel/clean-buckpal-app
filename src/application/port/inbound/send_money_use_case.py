from abc import ABC, abstractmethod

from src.application.port.inbound.send_money_command import SendMoneyCommand
from src.application.domain.model.activity import Activity


class SendMoneyUseCase(ABC):
    """
    Use case for sending money from one account to another.
    This use case is responsible for orchestrating the process of sending money
    between accounts. It uses the SendMoneyService to perform the actual
    transaction and the UpdateAccountStatePort to update the state of the accounts
    after the transaction.
    """

    @abstractmethod
    def send_money(self, send_money_command: SendMoneyCommand) -> Activity:
        pass
