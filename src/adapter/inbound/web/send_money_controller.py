from dependency_injector.wiring import inject

from src.application.port.inbound.send_money_use_case import SendMoneyUseCase
from src.adapter.inbound.web.web_model import (
    WebMapper,
    SendMoneyRequest,
    SendMoneyResponse,
)
from src.common.log import logger


class SendMoneyController:
    """
    Controller for sending money between accounts.
    This controller is responsible for handling the request to send
    money between accounts. It uses the SendMoneyUseCase to perform
    the money transfer operation.
    Attributes:
        send_money_use_case: Use case for sending money between accounts.
    """

    @inject
    def __init__(self, send_money_use_case: SendMoneyUseCase):
        self._send_money_use_case = send_money_use_case

    def send_money(self, send_money_request: SendMoneyRequest) -> SendMoneyResponse:
        logger.info("Processing send money request: %s", send_money_request)
        send_money_command = WebMapper.map_to_send_money_command(send_money_request)
        activity = self._send_money_use_case.send_money(send_money_command)
        result = WebMapper.map_to_send_money_entity(activity)
        logger.info("Send money result: %s", result)
        return result
