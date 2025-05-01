from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.common.log import logger
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
from src.adapter.inbound.web.send_money_controller import SendMoneyController
from src.adapter.inbound.web.list_account_controller import ListAccountController
from src.adapter.inbound.web.list_activity_controller import ListActivityController
from src.adapter.inbound.web.get_account_balance_controller import (
    GetAccountBalanceController,
)
from src.adapter.inbound.web.insert_account_controller import (
    InsertAccountController,
)
from src.application.port.inbound.send_money_use_case import SendMoneyUseCase
from src.application.port.inbound.list_account_use_case import ListAccountUseCase
from src.application.port.inbound.list_activity_use_case import ListActivityUseCase
from src.application.port.inbound.get_account_balance_use_case import (
    GetAccountBalanceUseCase,
)
from src.application.port.inbound.insert_account_use_case import InsertAccountUseCase
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
    AccountResponse,
    SendMoneyResponse,
    ActivityResponse,
    GetAccountBalanceResponse,
    InsertAccountResponse,
    Mapper,
)

app = FastAPI()
IN_MEMORY_DATA_ACCOUNT_REPOSITORY = InMemoryDataAccountRepository()
IN_MEMORY_DATA_ACTIVITY_REPOSITORY = InMemoryDataActivityRepository()
PERSISTENCE_ADAPTER = AccountPersistenceAdapter(
    IN_MEMORY_DATA_ACCOUNT_REPOSITORY, IN_MEMORY_DATA_ACTIVITY_REPOSITORY
)


class SendMoneyRequest(BaseModel):
    source_account_id: int
    target_account_id: int
    amount: float


class CreateAccountRequest(BaseModel):
    account_id: int
    amount: float


# Dependency injection for the controller
def send_money_controller():
    account_lock = InMemoryAccountLock()

    money_transfer_properties = MoneyTransferProperties()

    send_money_service: SendMoneyUseCase = SendMoneyService(
        load_account_port=PERSISTENCE_ADAPTER,
        account_lock=account_lock,
        update_account_state_port=PERSISTENCE_ADAPTER,
        money_transfer_properties=money_transfer_properties,
    )

    return SendMoneyController(send_money_service)


def get_account_controller():
    list_account_service: ListAccountUseCase = ListAccountService(PERSISTENCE_ADAPTER)

    return ListAccountController(list_account_service)


def get_activity_controller():
    list_activity_service: ListActivityUseCase = ListActivityService(
        PERSISTENCE_ADAPTER
    )

    return ListActivityController(list_activity_service)


def get_account_balance_controller():
    get_account_balance_service: GetAccountBalanceUseCase = GetAccountBalanceService(
        PERSISTENCE_ADAPTER
    )

    return GetAccountBalanceController(get_account_balance_service)


def insert_account_controller():
    insert_account_service: InsertAccountUseCase = InsertAccountService(
        PERSISTENCE_ADAPTER
    )

    return InsertAccountController(insert_account_service)


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


@app.get("/account", response_model=list[AccountResponse])
async def get_account(
    controller: ListAccountController = Depends(get_account_controller),
):
    accounts = controller.list_account()
    return [Mapper.map_to_account_entity(account) for account in accounts]


@app.get("/activity", response_model=list[ActivityResponse])
async def get_activity(
    controller: ListActivityController = Depends(get_activity_controller),
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


@app.post("/account", response_model=InsertAccountResponse)
async def create_account(
    request: CreateAccountRequest,
    controller: InsertAccountController = Depends(insert_account_controller),
):
    account = controller.insert_account(request.account_id, request.amount)
    return Mapper.map_to_insert_account_entity(account)
