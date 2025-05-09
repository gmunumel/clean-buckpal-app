# pylint: disable=c-extension-no-member
from dependency_injector import containers, providers

from src.adapter.inbound.web.send_money_controller import SendMoneyController
from src.adapter.inbound.web.list_account_controller import ListAccountController
from src.adapter.inbound.web.list_activity_controller import ListActivityController
from src.adapter.inbound.web.get_account_balance_controller import (
    GetAccountBalanceController,
)
from src.adapter.inbound.web.insert_account_controller import InsertAccountController
from src.application.domain.service.money_transfer_properties import (
    MoneyTransferProperties,
)
from src.application.domain.service.send_money_service import SendMoneyService
from src.application.domain.service.list_account_service import ListAccountService
from src.application.domain.service.list_activity_service import ListActivityService
from src.application.domain.service.get_account_balance_service import (
    GetAccountBalanceService,
)
from src.application.domain.service.insert_account_service import InsertAccountService
from src.adapter.outbound.persistence.in_memory_data_account_repository import (
    InMemoryDataAccountRepository,
)
from src.adapter.outbound.persistence.in_memory_data_activity_repository import (
    InMemoryDataActivityRepository,
)
from src.adapter.outbound.persistence.in_memory_account_lock import (
    InMemoryAccountLock,
)
from src.adapter.outbound.persistence.account_persistence_adapter import (
    AccountPersistenceAdapter,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.adapter.inbound.web.endpoints"]
    )

    # Outbound adapters
    in_memory_data_account_repository = providers.Singleton(
        InMemoryDataAccountRepository
    )
    in_memory_data_activity_repository = providers.Singleton(
        InMemoryDataActivityRepository
    )
    account_lock = providers.Singleton(InMemoryAccountLock)

    # Persistence adapter
    persistence_adapter = providers.Singleton(
        AccountPersistenceAdapter,
        account_repository=in_memory_data_account_repository,
        activity_repository=in_memory_data_activity_repository,
    )

    # Domain services
    money_transfer_properties = providers.Factory(MoneyTransferProperties)
    send_money_service = providers.Factory(
        SendMoneyService,
        load_account_port=persistence_adapter,
        account_lock=account_lock,
        update_account_state_port=persistence_adapter,
        money_transfer_properties=money_transfer_properties,
    )
    list_account_service = providers.Factory(
        ListAccountService,
        list_account_port=persistence_adapter,
    )
    list_activity_service = providers.Factory(
        ListActivityService,
        list_activity_port=persistence_adapter,
    )
    get_account_balance_service = providers.Factory(
        GetAccountBalanceService,
        load_account_port=persistence_adapter,
    )
    insert_account_service = providers.Factory(
        InsertAccountService,
        insert_account_port=persistence_adapter,
    )

    # Controllers
    send_money_controller = providers.Factory(
        SendMoneyController,
        send_money_use_case=send_money_service,
    )
    list_account_controller = providers.Factory(
        ListAccountController,
        list_account_use_case=list_account_service,
    )
    list_activity_controller = providers.Factory(
        ListActivityController,
        list_activity_use_case=list_activity_service,
    )
    get_account_balance_controller = providers.Factory(
        GetAccountBalanceController,
        get_account_balance_use_case=get_account_balance_service,
    )
    insert_account_controller = providers.Factory(
        InsertAccountController,
        insert_account_use_case=insert_account_service,
    )
