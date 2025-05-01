from src.application.port.inbound.insert_account_use_case import InsertAccountUseCase
from src.application.port.inbound.insert_account_command import InsertAccountCommand
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money
from src.application.domain.model.account import Account


class InsertAccountController:
    """
    Controller for inserting a new account.
    This controller is responsible for handling the request to create
    a new account. It uses the InsertAccountUseCase to perform the
    insertion of the account based on the provided command.
    Attributes:
        insert_account: Use case for inserting a new account.
    """

    def __init__(self, insert_account_use_case: InsertAccountUseCase):
        self._insert_account_use_case = insert_account_use_case

    def insert_account(self, account_id: int, money: float) -> Account:
        insert_account_command = InsertAccountCommand(
            AccountId(account_id), Money.of(money)
        )
        return self._insert_account_use_case.insert_account(insert_account_command)
