from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.common.log import logger
from src.application.domain.service.money_transfer_properties import (
    MoneyTransferProperties,
)
from src.application.domain.service.send_money_service import SendMoneyService
from src.application.domain.service.get_account_service import GetAccountService
from src.application.domain.service.get_activity_service import GetActivityService
from src.application.domain.service.get_account_balance_service import (
    GetAccountBalanceService,
)
from src.application.domain.service.create_account_service import CreateAccountService
from src.adapter.inbound.web.send_money_controller import SendMoneyController
from src.adapter.inbound.web.get_account_controller import GetAccountController
from src.adapter.inbound.web.get_activity_controller import GetActivityController
from src.adapter.inbound.web.get_account_balance_controller import (
    GetAccountBalanceController,
)
from src.adapter.inbound.web.create_account_controller import (
    CreateAccountController,
)
from src.application.port.inbound.send_money_use_case import SendMoneyUseCase
from src.application.port.inbound.get_account_use_case import GetAccountUseCase
from src.application.port.inbound.get_activity_use_case import GetActivityUseCase
from src.application.port.inbound.get_account_balance_use_case import (
    GetAccountBalanceUseCase,
)
from src.application.port.inbound.create_account_use_case import CreateAccountUseCase
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
from src.adapter.outbound.persistence.mapper import (
    GetAccountResponse,
    SendMoneyResponse,
    GetActivityResponse,
    GetAccountBalanceResponse,
    CreateAccountResponse,
    Mapper,
)

app = FastAPI()


class SendMoneyRequest(BaseModel):
    source_account_id: int
    target_account_id: int
    amount: float


class CreateAccountRequest(BaseModel):
    account_id: int
    amount: float


# Dependency injection for the controller
def send_money_controller():
    in_memory_data_account_repository = InMemoryDataAccountRepository()
    in_memory_data_activity_repository = InMemoryDataActivityRepository()

    persistence_adapter = AccountPersistenceAdapter(
        in_memory_data_account_repository, in_memory_data_activity_repository
    )

    account_lock = InMemoryAccountLock()

    money_transfer_properties = MoneyTransferProperties()

    send_money_service: SendMoneyUseCase = SendMoneyService(
        load_account_port=persistence_adapter,
        account_lock=account_lock,
        update_account_state_port=persistence_adapter,
        money_transfer_properties=money_transfer_properties,
    )

    return SendMoneyController(send_money_service)


def get_account_controller():
    in_memory_data_account_repository = InMemoryDataAccountRepository()
    in_memory_data_activity_repository = InMemoryDataActivityRepository()

    persistence_adapter = AccountPersistenceAdapter(
        in_memory_data_account_repository, in_memory_data_activity_repository
    )

    list_account_service: GetAccountUseCase = GetAccountService(persistence_adapter)

    return GetAccountController(list_account_service)


def get_activity_controller():
    in_memory_data_account_repository = InMemoryDataAccountRepository()
    in_memory_data_activity_repository = InMemoryDataActivityRepository()

    persistence_adapter = AccountPersistenceAdapter(
        in_memory_data_account_repository, in_memory_data_activity_repository
    )

    list_activity_service: GetActivityUseCase = GetActivityService(persistence_adapter)

    return GetActivityController(list_activity_service)


def get_account_balance_controller():
    in_memory_data_account_repository = InMemoryDataAccountRepository()
    in_memory_data_activity_repository = InMemoryDataActivityRepository()

    persistence_adapter = AccountPersistenceAdapter(
        in_memory_data_account_repository, in_memory_data_activity_repository
    )

    get_account_balance_service: GetAccountBalanceUseCase = GetAccountBalanceService(
        persistence_adapter
    )

    return GetAccountBalanceController(get_account_balance_service)


def create_account_controller():
    in_memory_data_account_repository = InMemoryDataAccountRepository()
    in_memory_data_activity_repository = InMemoryDataActivityRepository()

    persistence_adapter = AccountPersistenceAdapter(
        in_memory_data_account_repository, in_memory_data_activity_repository
    )

    create_account_service: CreateAccountUseCase = CreateAccountService(
        persistence_adapter
    )

    return CreateAccountController(create_account_service)


@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError):
    logger.error("ValueError: %s", exc)
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(_request: Request, exc: Exception):
    logger.error("Unhandled Exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


@app.post("/send-money", response_model=SendMoneyResponse)
async def send_money(
    request: SendMoneyRequest,
    controller: SendMoneyController = Depends(send_money_controller),
):
    success = controller.send_money(
        source_account_id=request.source_account_id,
        target_account_id=request.target_account_id,
        amount=request.amount,
    )
    if success:
        return SendMoneyResponse(success=True, message="Money sent successfully.")
    return SendMoneyResponse(success=False, message="Insufficient funds.")


@app.get("/account", response_model=list[GetAccountResponse])
async def get_account(
    controller: GetAccountController = Depends(get_account_controller),
):
    accounts = controller.list_account()
    return [Mapper.map_to_account_entity(account) for account in accounts]


@app.get("/activity", response_model=list[GetActivityResponse])
async def get_activity(
    controller: GetActivityController = Depends(get_activity_controller),
):
    activities = controller.list_activity()
    return [Mapper.map_to_activity_entity(activity) for activity in activities]


@app.get("/account-balance/{account_id}", response_model=GetAccountBalanceResponse)
async def get_account_balance(
    account_id: int,
    controller: GetAccountBalanceController = Depends(get_account_balance_controller),
):
    account_balance = controller.get_account_balance(account_id)
    return Mapper.map_to_get_account_balance_entity(account_id, account_balance)


@app.post("/account", response_model=CreateAccountResponse)
async def create_account(
    request: CreateAccountRequest,
    controller: CreateAccountController = Depends(create_account_controller),
):
    controller.create_account(request.account_id, request.amount)
    return Mapper.map_to_create_account_entity(request.account_id, request.amount)
