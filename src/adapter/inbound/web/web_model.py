from pydantic import BaseModel

from src.application.port.inbound.send_money_command import SendMoneyCommand
from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId
from src.application.domain.model.money import Money
from src.application.domain.model.user_id import UserId
from src.application.domain.model.name import Name
from src.application.domain.model.user import User
from src.application.domain.model.address import Address
from src.application.port.inbound.get_account_balance_query import (
    GetAccountBalanceQuery,
)
from src.application.port.inbound.list_account_query import ListAccountQuery
from src.application.port.inbound.list_activity_query import ListActivityQuery
from src.application.port.inbound.list_user_query import ListUserQuery
from src.application.port.inbound.update_account_command import UpdateAccountCommand
from src.application.port.inbound.register_user_command import RegisterUserCommand


class SendMoneyRequest(BaseModel):
    source_account_id: int
    target_account_id: int
    amount: float


class GetAccountBalanceParam(BaseModel):
    account_id: int


class ListAccountParam(BaseModel):
    account_id: int | None = None


class ListActivityParam(BaseModel):
    activity_id: int | None = None


class ListUserParam(BaseModel):
    user_id: int | None = None


class UpdateAccountRequest(BaseModel):
    amount: float


class AddressRequestResponse(BaseModel):
    street_name: str
    street_number: int
    city: str
    postal_code: str
    country: str


class RegisterUserRequest(BaseModel):
    user_id: int
    name: str
    address: AddressRequestResponse


class SendMoneyResponse(BaseModel):
    source_account_id: int
    target_account_id: int
    amount: float


class ActivityResponse(BaseModel):
    activity_id: int | None
    owner_account_id: int
    source_account_id: int
    target_account_id: int
    timestamp: str
    money: float


class AccountResponse(BaseModel):
    account_id: int
    baseline_balance: float
    activity_window: list[ActivityResponse]


class UserResponse(BaseModel):
    user_id: int
    name: str
    address: AddressRequestResponse
    status: str


class GetAccountBalanceResponse(BaseModel):
    account_id: int
    balance: float


class DepositMoneyResponse(BaseModel):
    account_id: int
    amount: float


class UpdateAccountResponse(GetAccountBalanceResponse):
    pass


class RegisterUserResponse(BaseModel):
    user_id: int
    name: str
    address: AddressRequestResponse


class WebMapper:
    @staticmethod
    def map_to_send_money_command(
        send_money_request: SendMoneyRequest,
    ) -> SendMoneyCommand:
        return SendMoneyCommand(
            source_account_id=AccountId(send_money_request.source_account_id),
            target_account_id=AccountId(send_money_request.target_account_id),
            money=Money.of(send_money_request.amount),
        )

    @staticmethod
    def map_to_get_account_balance_query(
        get_account_balance_request: GetAccountBalanceParam,
    ) -> GetAccountBalanceQuery:
        return GetAccountBalanceQuery(AccountId(get_account_balance_request.account_id))

    @staticmethod
    def map_to_list_account_query(
        list_account_param: ListAccountParam,
    ) -> ListAccountQuery:
        account_id = list_account_param.account_id
        account_id_or_none = AccountId(account_id) if account_id else None
        return ListAccountQuery(account_id_or_none)

    @staticmethod
    def map_to_list_user_query(
        list_user_param: ListUserParam,
    ) -> ListUserQuery:
        user_id = list_user_param.user_id
        user_id_or_none = UserId(user_id) if user_id else None
        return ListUserQuery(user_id_or_none)

    @staticmethod
    def map_to_list_activity_query(
        list_activity_param: ListActivityParam,
    ) -> ListActivityQuery:
        activity_id = list_activity_param.activity_id
        activity_id_or_none = ActivityId(activity_id) if activity_id else None
        return ListActivityQuery(activity_id_or_none)

    @staticmethod
    def map_to_update_account_command(account_id: int,
        update_account_request: UpdateAccountRequest,
    ) -> UpdateAccountCommand:
        return UpdateAccountCommand(
            AccountId(account_id),
            Money.of(update_account_request.amount),
        )

    @staticmethod
    def map_to_register_user_command(
        register_user_request: RegisterUserRequest,
    ) -> RegisterUserCommand:
        return RegisterUserCommand(
            UserId(register_user_request.user_id),
            Name(register_user_request.name),
            Address(
                street_name=register_user_request.address.street_name,
                street_number=register_user_request.address.street_number,
                city=register_user_request.address.city,
                postal_code=register_user_request.address.postal_code,
                country=register_user_request.address.country,
            ),
        )

    @staticmethod
    def map_to_account_entity(account: Account) -> AccountResponse:
        account_id = account.id
        activity_windows = account.activity_window
        activities = []
        for activity in activity_windows.activities:
            activities.append(WebMapper.map_to_activity_entity(activity))
        account_baseline_balance = account.baseline_balance
        return AccountResponse(
            account_id=account_id.id,
            baseline_balance=account_baseline_balance.amount,
            activity_window=activities,
        )

    @staticmethod
    def map_to_activity_entity(activity: Activity) -> ActivityResponse:
        activity_id = activity.id
        activity_owner_account_id = activity.owner_account_id
        activity_source_account_id = activity.source_account_id
        activity_target_account_id = activity.target_account_id
        activity_timestamp = activity.timestamp
        activity_money = activity.money
        return ActivityResponse(
            activity_id=activity_id.id,
            owner_account_id=activity_owner_account_id.id,
            source_account_id=activity_source_account_id.id,
            target_account_id=activity_target_account_id.id,
            timestamp=activity_timestamp.isoformat(),
            money=activity_money.amount,
        )

    @staticmethod
    def map_to_get_account_balance_entity(
        account_id: int, account_balance: Money
    ) -> GetAccountBalanceResponse:
        return GetAccountBalanceResponse(
            account_id=account_id, balance=account_balance.amount
        )

    @staticmethod
    def map_to_update_account_entity(account: Account) -> UpdateAccountResponse:
        account_id = account.id
        balance = account.baseline_balance
        return UpdateAccountResponse(account_id=account_id.id, balance=balance.amount)

    @staticmethod
    def map_to_send_money_entity(activity: Activity) -> SendMoneyResponse:
        activity_source_account_id = activity.source_account_id
        activity_target_account_id = activity.target_account_id
        activity_money = activity.money
        return SendMoneyResponse(
            source_account_id=activity_source_account_id.id,
            target_account_id=activity_target_account_id.id,
            amount=activity_money.amount,
        )

    @staticmethod
    def map_to_register_user_entity(user: User) -> RegisterUserResponse:
        user_id = user.id
        user_name = user.name
        address = user.address
        return RegisterUserResponse(
            user_id=user_id.id,
            name=user_name.full_name,
            address=WebMapper.map_to_address_entity(address),
        )

    @staticmethod
    def map_to_address_entity(address: Address) -> AddressRequestResponse:
        return AddressRequestResponse(
            street_name=address.street_name,
            street_number=address.street_number,
            city=address.city,
            postal_code=address.postal_code,
            country=address.country,
        )

    @staticmethod
    def map_to_user_entity(user: User) -> UserResponse:
        user_id = user.id
        user_name = user.name
        address = user.address
        status = user.status
        return UserResponse(
            user_id=user_id.id,
            name=user_name.full_name,
            address=WebMapper.map_to_address_entity(address),
            status=str(status),
        )
