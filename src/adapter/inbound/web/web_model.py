from pydantic import BaseModel

from src.application.port.inbound.send_money_command import SendMoneyCommand
from src.application.domain.model.account import Account
from src.application.domain.model.account_id import AccountId
from src.application.domain.model.activity import Activity
from src.application.domain.model.activity_id import ActivityId
from src.application.domain.model.money import Money
from src.application.port.inbound.get_account_balance_query import (
    GetAccountBalanceQuery,
)
from src.application.port.inbound.list_account_query import ListAccountQuery
from src.application.port.inbound.list_activity_query import ListActivityQuery
from src.application.port.inbound.insert_account_command import InsertAccountCommand


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


class InsertAccountRequest(BaseModel):
    account_id: int
    amount: float


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


class GetAccountBalanceResponse(BaseModel):
    account_id: int
    balance: float


class DepositMoneyResponse(BaseModel):
    account_id: int
    amount: float


class InsertAccountResponse(GetAccountBalanceResponse):
    pass


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
    def map_to_list_activity_query(
        list_activity_param: ListActivityParam,
    ) -> ListActivityQuery:
        activity_id = list_activity_param.activity_id
        activity_id_or_none = ActivityId(activity_id) if activity_id else None
        return ListActivityQuery(activity_id_or_none)

    @staticmethod
    def map_to_insert_account_command(
        insert_account_request: InsertAccountRequest,
    ) -> InsertAccountCommand:
        return InsertAccountCommand(
            AccountId(insert_account_request.account_id),
            Money.of(insert_account_request.amount),
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
    def map_to_insert_account_entity(account: Account) -> InsertAccountResponse:
        account_id = account.id
        balance = account.baseline_balance
        return InsertAccountResponse(account_id=account_id.id, balance=balance.amount)

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
