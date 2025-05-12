from typing import Callable, Dict, List, Type
from dependency_injector.wiring import Provide, inject

from src.application.domain.model.event import Event, UserRegisteredEvent
from src.application.domain.model.money import Money
from src.application.domain.model.account_id import AccountId
from src.application.port.inbound.insert_account_command import (
    InsertAccountCommand,
)
from src.application.domain.service.insert_account_service import InsertAccountService
from src.common.log import logger


@inject
def handle_user_registered_event(
    event: UserRegisteredEvent,
    insert_account_service: InsertAccountService = Provide["insert_account_service"],
):
    logger.info("UserRegisteredEvent received for user_id: %s", event.user_id)
    insert_account_command = InsertAccountCommand(AccountId(event.user_id), Money.of(0))
    insert_account_service.insert_account(insert_account_command)


HANDLERS: Dict[Type[Event], List[Callable]] = {
    UserRegisteredEvent: [handle_user_registered_event],
}
