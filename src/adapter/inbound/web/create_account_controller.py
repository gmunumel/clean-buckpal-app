from src.application.port.inbound.create_account_use_case import CreateAccountUseCase
from src.application.port.inbound.create_account_command import CreateAccountCommand
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money


class CreateAccountController:
    """
    Controller for inserting a new account.
    This controller is responsible for handling the request to create
    a new account. It uses the CreateAccountUseCase to perform the
    insertion of the account based on the provided command.
    Attributes:
        create_account: Use case for inserting a new account.
    """

    def __init__(self, insert_account_use_case: CreateAccountUseCase):
        self._insert_account_use_case = insert_account_use_case

    def create_account(self, account_id: int, money: float):
        insert_account_command = CreateAccountCommand(
            AccountId(account_id), Money.of(money)
        )
        return self._insert_account_use_case.insert_account(insert_account_command)
