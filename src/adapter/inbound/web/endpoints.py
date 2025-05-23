from fastapi import APIRouter, Response, status, Depends
from dependency_injector.wiring import Provide, inject

from src.common.container import Container
from src.application.domain.model.user import User
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
from src.adapter.inbound.web.jwt_utils import authenticate_user
from src.adapter.inbound.web.web_model import (
    GetAccountBalanceParam,
    ListAccountParam,
    ListActivityParam,
    AccountResponse,
    SendMoneyRequestResponse,
    ActivityResponse,
    GetAccountBalanceResponse,
    UpdateAccountRequest,
    RegisterUserRequest,
    RegisterUserResponse,
    ListUserParam,
    UserResponse,
    LoginUserRequest,
    LoginUserResponse,
)


router = APIRouter()


@router.post("/send-money", response_model=SendMoneyRequestResponse)
@inject
async def send_money(
    request: SendMoneyRequestResponse,
    controller: SendMoneyController = Depends(Provide[Container.send_money_controller]),
    _authenticate_user: User = Depends(authenticate_user),
):
    return controller.send_money(request)


@router.get("/accounts", response_model=list[AccountResponse])
@inject
async def get_account(
    account_id: int | None = None,
    controller: ListAccountController = Depends(
        Provide[Container.list_account_controller]
    ),
    _authenticate_user: User = Depends(authenticate_user),
):
    query_param = ListAccountParam(account_id=account_id)
    return controller.list_account(query_param)


@router.get("/activities", response_model=list[ActivityResponse])
@inject
async def get_activity(
    activity_id: int | None = None,
    controller: ListActivityController = Depends(
        Provide[Container.list_activity_controller]
    ),
    _authenticate_user: User = Depends(authenticate_user),
):
    query_params = ListActivityParam(activity_id=activity_id)
    return controller.list_activity(query_params)


@router.get("/accounts-balance/{account_id}", response_model=GetAccountBalanceResponse)
@inject
async def get_account_balance(
    account_id: int,
    controller: GetAccountBalanceController = Depends(
        Provide[Container.get_account_balance_controller]
    ),
    _authenticate_user: User = Depends(authenticate_user),
):
    path_param = GetAccountBalanceParam(account_id=account_id)
    return controller.get_account_balance(path_param)


@router.put(
    "/accounts/{account_id}",
    response_model=AccountResponse | dict,
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
    _authenticate_user: User = Depends(authenticate_user),
) -> AccountResponse | dict[str, object]:
    account = controller.update_account(account_id, request)
    if account:
        return account
    response.status_code = status.HTTP_204_NO_CONTENT
    return {}


@router.post("/users", response_model=RegisterUserResponse)
@inject
async def register_user(
    request: RegisterUserRequest,
    controller: RegisterUserController = Depends(
        Provide[Container.register_user_controller]
    ),
):
    return controller.register_user(request)


@router.get("/users", response_model=list[UserResponse])
@inject
async def get_user(
    user_id: int | None = None,
    controller: ListUserController = Depends(Provide[Container.list_user_controller]),
    _authenticate_user: User = Depends(authenticate_user),
):
    query_param = ListUserParam(user_id=user_id)
    return controller.list_user(query_param)


@router.post("/login", response_model=LoginUserResponse)
@inject
async def login(
    request: LoginUserRequest,
    controller: LoginUserController = Depends(Provide[Container.login_user_controller]),
):
    return controller.login_user(request)
