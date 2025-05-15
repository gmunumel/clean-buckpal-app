from fastapi import APIRouter, Response, status, Depends
from dependency_injector.wiring import Provide, inject

from src.common.container import Container

from src.adapter.inbound.web.send_money_controller import SendMoneyController
from src.adapter.inbound.web.list_account_controller import ListAccountController
from src.adapter.inbound.web.list_activity_controller import ListActivityController
from src.adapter.inbound.web.get_account_balance_controller import (
    GetAccountBalanceController,
)
from src.adapter.inbound.web.update_account_controller import (
    UpdateAccountController,
)
from src.adapter.inbound.web.register_user_controller import (
    RegisterUserController,
)
from src.adapter.inbound.web.list_user_controller import (
    ListUserController,
)
from src.adapter.inbound.web.web_model import (
    SendMoneyRequest,
    GetAccountBalanceParam,
    ListAccountParam,
    ListActivityParam,
    AccountResponse,
    SendMoneyResponse,
    ActivityResponse,
    GetAccountBalanceResponse,
    UpdateAccountRequest,
    UpdateAccountResponse,
    RegisterUserRequest,
    RegisterUserResponse,
    ListUserParam,
    UserResponse,
)


router = APIRouter()


@router.post("/send-money", response_model=SendMoneyResponse)
@inject
async def send_money(
    request: SendMoneyRequest,
    controller: SendMoneyController = Depends(Provide[Container.send_money_controller]),
):
    return controller.send_money(request)


@router.get("/account", response_model=list[AccountResponse])
@inject
async def get_account(
    account_id: int | None = None,
    controller: ListAccountController = Depends(
        Provide[Container.list_account_controller]
    ),
):
    query_param = ListAccountParam(account_id=account_id)
    return controller.list_account(query_param)


@router.get("/activity", response_model=list[ActivityResponse])
@inject
async def get_activity(
    activity_id: int | None = None,
    controller: ListActivityController = Depends(
        Provide[Container.list_activity_controller]
    ),
):
    query_params = ListActivityParam(activity_id=activity_id)
    return controller.list_activity(query_params)


@router.get("/account-balance/{account_id}", response_model=GetAccountBalanceResponse)
@inject
async def get_account_balance(
    account_id: int,
    controller: GetAccountBalanceController = Depends(
        Provide[Container.get_account_balance_controller]
    ),
):
    path_param = GetAccountBalanceParam(account_id=account_id)
    return controller.get_account_balance(path_param)


@router.put(
    "/account/{account_id}",
    response_model=UpdateAccountResponse | dict,
    status_code=201,
)
@inject
async def create_or_update_account(
    account_id: int,
    request: UpdateAccountRequest,
    response: Response,
    controller: UpdateAccountController = Depends(
        Provide[Container.update_account_controller]
    ),
):
    account = controller.update_account(account_id, request)
    if account:
        return account
    response.status_code = status.HTTP_204_NO_CONTENT
    return {}


@router.post("/user", response_model=RegisterUserResponse)
@inject
async def register_user(
    request: RegisterUserRequest,
    controller: RegisterUserController = Depends(
        Provide[Container.register_user_controller]
    ),
):
    return controller.register_user(request)


@router.get("/user", response_model=list[UserResponse])
@inject
async def get_user(
    user_id: int | None = None,
    controller: ListUserController = Depends(Provide[Container.list_user_controller]),
):
    query_param = ListUserParam(user_id=user_id)
    return controller.list_user(query_param)
