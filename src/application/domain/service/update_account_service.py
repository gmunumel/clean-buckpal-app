from src.application.port.inbound.update_account_use_case import (
    UpdateAccountUseCase,
)
from src.application.port.inbound.update_account_command import (
    UpdateAccountCommand,
)
from src.application.port.outbound.update_account_port import (
    UpdateAccountPort,
)
from src.application.domain.model.account import Account


class UpdateAccountService(UpdateAccountUseCase):
    """
    Service for updating a new account.
    This service uses the UpdateAccountPort to update an account in the data source.
    It provides a method to update an account based on the provided UpdateAccountCommand.
    Attributes:
        update_account_port: Port for updating an account.
    """

    def __init__(self, update_account_port: UpdateAccountPort):
        self._update_account_port = update_account_port

    def update_account(
        self, update_account_command: UpdateAccountCommand
    ) -> Account | dict[str, object]:
        return self._update_account_port.update_account(
            account_id=update_account_command.account_id,
            money=update_account_command.money,
        )
