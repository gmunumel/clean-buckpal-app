from src.application.port.inbound.update_account_use_case import UpdateAccountUseCase
from src.adapter.inbound.web.web_model import (
    WebMapper,
    UpdateAccountRequest,
    UpdateAccountResponse,
)


class UpdateAccountController:
    """
    Controller for updating an account.
    This controller handles the HTTP request for updating an account and
    delegates the request to the UpdateAccountUseCase.
    It provides a method to update an account based on the provided UpdateAccountRequest.
    Attributes:
        update_account_use_case: Use case for updating an account.
    """

    def __init__(self, update_account_use_case: UpdateAccountUseCase):
        self._update_account_use_case = update_account_use_case

    def update_account(
        self, account_id: int, update_account_request: UpdateAccountRequest
    ) -> UpdateAccountResponse | dict:
        update_account_command = WebMapper.map_to_update_account_command(
            account_id, update_account_request
        )
        account = self._update_account_use_case.update_account(update_account_command)
        if account:
            return WebMapper.map_to_update_account_entity(account)
        return {}
