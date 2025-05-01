from src.application.port.inbound.send_money_use_case import SendMoneyUseCase
from src.application.port.inbound.send_money_command import SendMoneyCommand
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.money import Money


class SendMoneyController:
    """
    Controller for sending money between accounts.
    This controller is responsible for handling the request to send money
    between accounts. It uses the SendMoneyUseCase to perform the actual
    transaction.
    Attributes:
        send_money_use_case: Use case for sending money.
    """

    def __init__(self, send_money_use_case: SendMoneyUseCase):
        self._send_money_use_case = send_money_use_case

    def send_money(
        self, source_account_id: int, target_account_id: int, amount: float
    ) -> bool:
        send_money_command = SendMoneyCommand(
            AccountId(source_account_id), AccountId(target_account_id), Money.of(amount)
        )
        return self._send_money_use_case.send_money(send_money_command)
