from src.application.port.inbound.insert_account_use_case import (
    InsertAccountUseCase,
)
from src.application.port.inbound.insert_account_command import (
    InsertAccountCommand,
)
from src.application.port.outbound.insert_account_port import (
    InsertAccountPort,
)
from src.application.domain.model.account import Account


class InsertAccountService(InsertAccountUseCase):
    """
    Service for inserting a new account.
    This service is responsible for handling the logic of inserting a new account
    into the system. It uses the InsertAccountCommand to specify the details of
    the account to be inserted.
    """

    def __init__(self, insert_account_port: InsertAccountPort):
        self._insert_account_port = insert_account_port

    def insert_account(self, insert_account_command: InsertAccountCommand) -> Account:
        return self._insert_account_port.insert_account(
            account_id=insert_account_command.account_id,
            money=insert_account_command.money,
        )
