from abc import ABC, abstractmethod

from src.application.port.inbound.deposit_money_command import DepositMoneyCommand


class DepositMoneyUseCase(ABC):
    """
    Use case for depositing money into an account.
    This use case is responsible for orchestrating the process of depositing money
    into an account. It uses the DepositMoneyCommand to specify the amount and
    account information for the deposit.
    Attributes:
        deposit_money_command: Command for depositing money.
    """

    @abstractmethod
    def deposit_money(self, deposit_money_command: DepositMoneyCommand) -> bool:
        pass
