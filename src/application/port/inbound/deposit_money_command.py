from dataclasses import dataclass

from src.application.domain.model.money import Money
from src.application.domain.model.account_id import AccountId


@dataclass(frozen=True)
class DepositMoneyCommand:
    """
    DepositMoneyCommand to deposit money into a bank account.
    """

    account_id: AccountId
    money: Money

    def __post_init__(self):
        if not self.account_id:
            raise ValueError("Account ID must be provided.")
        if not self.money:
            raise ValueError("Money amount must be provided.")
        if not self.money.is_positive():
            raise ValueError("Money amount must be greater than zero.")

    def get_account_id(self) -> AccountId:
        return self.account_id

    def get_money(self) -> Money:
        return self.money

    def __repr__(self):
        return (
            f"DepositMoneyCommand(account_id={self.account_id!r}, money={self.money!r})"
        )
