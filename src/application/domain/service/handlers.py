from typing import Callable, Dict, List, Type
from dependency_injector.wiring import Provide, inject

from src.application.domain.model.event import Event, UserRegisteredEvent
from src.application.domain.model.money import Money
from src.application.domain.model.account_id import AccountId
from src.application.port.inbound.update_account_command import (
    UpdateAccountCommand,
)
from src.application.domain.service.update_account_service import UpdateAccountService
from src.common.log import logger


@inject
def handle_user_registered_event(
    event: Event,
    update_account_service: UpdateAccountService = Provide["update_account_service"],
):
    if not isinstance(event, UserRegisteredEvent):
        logger.error("Received wrong event type: %s", type(event))
        return
    logger.info("UserRegisteredEvent received for user_id: %s", event.user_id)
    update_account_command = UpdateAccountCommand(AccountId(event.user_id), Money.of(0))
    update_account_service.update_account(update_account_command)


HANDLERS: Dict[Type[Event], List[Callable[[Event], None]]] = {
    UserRegisteredEvent: [handle_user_registered_event],
}
