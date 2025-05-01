from abc import ABC, abstractmethod

from src.application.port.inbound.create_account_command import (
    CreateAccountCommand,
)


class CreateAccountUseCase(ABC):
    @abstractmethod
    def insert_account(self, insert_account_command: CreateAccountCommand):
        pass
