from abc import ABC, abstractmethod

from src.application.port.inbound.update_account_command import (
    UpdateAccountCommand,
)
from src.application.domain.model.account import Account


class UpdateAccountUseCase(ABC):
    @abstractmethod
    def update_account(
        self, update_account_command: UpdateAccountCommand
    ) -> Account | dict[str, object]:
        pass
