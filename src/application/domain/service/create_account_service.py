from src.application.port.inbound.create_account_use_case import (
    CreateAccountUseCase,
)
from src.application.port.inbound.create_account_command import (
    CreateAccountCommand,
)
from src.application.port.outbound.create_account_port import (
    CreateAccountPort,
)


class CreateAccountService(CreateAccountUseCase):
    """
    Service for inserting a new account.
    This service is responsible for handling the logic of inserting a new account
    into the system. It uses the CreateAccountCommand to specify the details of
    the account to be inserted.
    """

    def __init__(self, insert_account_port: CreateAccountPort):
        self._insert_account_port = insert_account_port

    def insert_account(self, insert_account_command: CreateAccountCommand):
        self._insert_account_port.insert_account(
            account_id=insert_account_command.get_account_id(),
            money=insert_account_command.get_money(),
        )
