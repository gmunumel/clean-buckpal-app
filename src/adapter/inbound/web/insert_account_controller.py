from src.application.port.inbound.insert_account_use_case import InsertAccountUseCase
from src.adapter.inbound.web.web_model import (
    WebMapper,
    InsertAccountRequest,
    InsertAccountResponse,
)


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

    def insert_account(
        self, insert_account_request: InsertAccountRequest
    ) -> InsertAccountResponse:
        insert_account_command = WebMapper.map_to_insert_account_command(
            insert_account_request
        )
        account = self._insert_account_use_case.insert_account(insert_account_command)
        return WebMapper.map_to_insert_account_entity(account)
