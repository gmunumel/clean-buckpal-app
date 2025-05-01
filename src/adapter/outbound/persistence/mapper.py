from pydantic import BaseModel

from src.application.domain.model.account import Account
from src.application.domain.model.activity import Activity
from src.application.domain.model.money import Money


class SendMoneyResponse(BaseModel):
    source_account_id: int
    target_account_id: int
    amount: float
    activity_id: int


class GetActivityResponse(BaseModel):
    activity_id: int
    owner_account_id: int
    source_account_id: int
    target_account_id: int
    timestamp: str
    money: float


class GetAccountResponse(BaseModel):
    account_id: int
    baseline_balance: float
    activity_window: list[GetActivityResponse] = []


class GetAccountBalanceResponse(BaseModel):
    account_id: int
    balance: float


class DepositMoneyResponse(BaseModel):
    account_id: int
    amount: float


class CreateAccountResponse(GetAccountBalanceResponse):
    pass


class Mapper:
    @staticmethod
    def map_to_account_entity(account: Account) -> GetAccountResponse:
        account_id = account.get_id()
        activity_windows = account.get_activity_window()
        activities = []
        for activity in activity_windows.get_activities():
            activities.append(Mapper.map_to_activity_entity(activity))
        return GetAccountResponse(
            account_id=account_id.get_id(),
            baseline_balance=account.baseline_balance.amount,
            activity_window=activities,
        )

    @staticmethod
    def map_to_activity_entity(activity: Activity) -> GetActivityResponse:
        activity_id = activity.get_id()
        activity_owner_account_id = activity.get_owner_account_id()
        activity_source_account_id = activity.get_source_account_id()
        activity_target_account_id = activity.get_target_account_id()
        activity_timestamp = activity.get_timestamp()
        activity_money = activity.get_money()
        return GetActivityResponse(
            activity_id=activity_id.get_id(),
            owner_account_id=activity_owner_account_id.get_id(),
            source_account_id=activity_source_account_id.get_id(),
            target_account_id=activity_target_account_id.get_id(),
            timestamp=activity_timestamp.isoformat(),
            money=activity_money.get_amount(),
        )

    @staticmethod
    def map_to_get_account_balance_entity(
        account_id: int, account_balance: Money
    ) -> GetAccountBalanceResponse:
        return GetAccountBalanceResponse(
            account_id=account_id, balance=account_balance.get_amount()
        )

    @staticmethod
    def map_to_deposit_money_entity(
        account_id: int, amount: float
    ) -> DepositMoneyResponse:
        return DepositMoneyResponse(account_id=account_id, amount=amount)

    @staticmethod
    def map_to_create_account_entity(
        account_id: int, account_balance: Money
    ) -> CreateAccountResponse:
        return CreateAccountResponse(
            account_id=account_id, balance=account_balance.get_amount()
        )
