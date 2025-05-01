from dataclasses import dataclass

from src.application.domain.model.money import Money
from src.application.domain.model.account_id import AccountId


@dataclass(frozen=True)
class SendMoneyCommand:
    """
    SendMoneyCommand class representing a command to send money from one account to another.
    """

    source_account_id: AccountId
    target_account_id: AccountId
    money: Money

    def __post_init__(self):
        if not self.source_account_id or not self.target_account_id:
            raise ValueError("Source and target account IDs must be provided.")
        if not self.money:
            raise ValueError("Money amount must be provided.")
        if not self.money.is_positive():
            raise ValueError("Money amount must be greater than zero.")

    def get_source_account_id(self) -> AccountId:
        return self.source_account_id

    def get_target_account_id(self) -> AccountId:
        return self.target_account_id

    def get_money(self) -> Money:
        return self.money

    def __repr__(self) -> str:
        return (
            f"SendCommand(source_account_id={self.source_account_id!r}, "
            f"target_account_id={self.target_account_id!r}, "
            f"money={self.money!r})"
        )
