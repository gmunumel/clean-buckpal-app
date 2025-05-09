from dataclasses import dataclass

from src.application.domain.model.money import Money
from src.application.domain.model.account_id import AccountId


@dataclass(frozen=True)
class InsertAccountCommand:
    """
    InsertAccountCommand to create a new bank account with an initial balance.
    This command is used to insert a new account into the system.
    """

    account_id: AccountId
    money: Money

    def __post_init__(self):
        if not self.account_id:
            raise ValueError("Account ID must be provided.")
        if not self.money:
            raise ValueError("Money must be provided.")
        if not self.money.is_positive():
            raise ValueError("Money must be greater than zero.")

    def __repr__(self):
        return (
            f"InsertAccountCommand(account_id={self.account_id!r}, "
            f"money={self.money!r})"
        )
