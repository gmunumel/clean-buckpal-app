from abc import ABC, abstractmethod

from src.application.port.inbound.insert_account_command import (
    InsertAccountCommand,
)
from src.application.domain.model.account import Account


class InsertAccountUseCase(ABC):
    @abstractmethod
    def insert_account(self, insert_account_command: InsertAccountCommand) -> Account:
        pass
