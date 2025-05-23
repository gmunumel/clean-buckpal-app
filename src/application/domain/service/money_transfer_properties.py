from dataclasses import dataclass

from src.application.domain.model.money import Money


@dataclass(frozen=True)
class MoneyTransferProperties:
    """
    Properties for money transfer operations.
    This class contains the properties required for money transfer operations,
    such as the maximum threshold that can be transferred in a single transaction.
    """

    amount: float | None = None

    @property
    def max_transfer_threshold(self) -> Money:
        return Money.of(self.amount or 1_000_000)
