# pylint: disable=c-extension-no-member
from dependency_injector import containers, providers

from src.adapter.inbound.web.send_money_controller import SendMoneyController
from src.adapter.inbound.web.list_account_controller import ListAccountController
from src.adapter.inbound.web.list_activity_controller import ListActivityController
from src.adapter.inbound.web.get_account_balance_controller import (
    GetAccountBalanceController,
)
from src.adapter.inbound.web.update_account_controller import UpdateAccountController
from src.adapter.inbound.web.register_user_controller import RegisterUserController
from src.adapter.inbound.web.login_user_controller import LoginUserController
from src.adapter.inbound.web.list_user_controller import ListUserController
from src.application.domain.service.money_transfer_properties import (
    MoneyTransferProperties,
)
from src.application.domain.service.send_money_service import SendMoneyService
from src.application.domain.service.list_account_service import ListAccountService
from src.application.domain.service.list_activity_service import ListActivityService
from src.application.domain.service.get_account_balance_service import (
    GetAccountBalanceService,
)
from src.application.domain.service.register_user_service import RegisterUserService
from src.application.domain.service.login_user_service import LoginUserService
from src.application.domain.service.list_user_service import ListUserService
from src.application.domain.service.update_account_service import UpdateAccountService
from src.application.domain.service.event_dispatcher import EventDispatcher
from src.adapter.outbound.persistence.in_memory_data_account_repository import (
    InMemoryDataAccountRepository,
)
from src.adapter.outbound.persistence.in_memory_data_activity_repository import (
    InMemoryDataActivityRepository,
)
from src.adapter.outbound.persistence.in_memory_account_lock import InMemoryAccountLock
from src.adapter.outbound.persistence.in_memory_data_user_repository import (
    InMemoryDataUserRepository,
)
from src.adapter.outbound.persistence.account_persistence_adapter import (
    AccountPersistenceAdapter,
)
from src.adapter.outbound.persistence.user_persistence_adapter import (
    UserPersistenceAdapter,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.adapter.inbound.web.endpoints",
            "src.application.domain.service.handlers",
        ]
    )

    # Outbound adapters
    in_memory_data_account_repository = providers.Singleton(
        InMemoryDataAccountRepository
    )
    in_memory_data_activity_repository = providers.Singleton(
        InMemoryDataActivityRepository
    )
    in_memory_data_user_repository = providers.Singleton(InMemoryDataUserRepository)
    account_lock = providers.Singleton(InMemoryAccountLock)

    # Persistence adapter
    persistence_adapter_account = providers.Singleton(
        AccountPersistenceAdapter,
        account_repository=in_memory_data_account_repository,
        activity_repository=in_memory_data_activity_repository,
    )
    persistence_adapter_user = providers.Singleton(
        UserPersistenceAdapter,
        user_repository=in_memory_data_user_repository,
    )
    event_dispatcher = providers.Singleton(EventDispatcher)

    # Domain services
    money_transfer_properties = providers.Factory(MoneyTransferProperties)
    send_money_service = providers.Factory(
        SendMoneyService,
        load_account_port=persistence_adapter_account,
        account_lock=account_lock,
        update_account_state_port=persistence_adapter_account,
        money_transfer_properties=money_transfer_properties,
    )
    list_account_service = providers.Factory(
        ListAccountService,
        list_account_port=persistence_adapter_account,
    )
    list_activity_service = providers.Factory(
        ListActivityService,
        list_activity_port=persistence_adapter_account,
    )
    get_account_balance_service = providers.Factory(
        GetAccountBalanceService,
        load_account_port=persistence_adapter_account,
    )
    update_account_service = providers.Factory(
        UpdateAccountService,
        update_account_port=persistence_adapter_account,
    )
    list_user_service = providers.Factory(
        ListUserService,
        list_user_port=persistence_adapter_user,
    )
    register_user_service = providers.Factory(
        RegisterUserService,
        register_user_port=persistence_adapter_user,
        event_dispatcher=event_dispatcher,
    )
    login_user_service = providers.Factory(
        LoginUserService,
        login_user_port=persistence_adapter_user,
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
    update_account_controller = providers.Factory(
        UpdateAccountController,
        update_account_use_case=update_account_service,
    )
    list_user_controller = providers.Factory(
        ListUserController,
        list_user_use_case=list_user_service,
    )
    register_user_controller = providers.Factory(
        RegisterUserController,
        register_user_use_case=register_user_service,
    )
    login_user_controller = providers.Factory(
        LoginUserController,
        login_user_use_case=login_user_service,
    )
