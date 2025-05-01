from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    """
    Money class representing a monetary value.
    This class is immutable and provides methods for basic arithmetic operations.
    """

    amount: float

    @classmethod
    def add(cls, money: "Money", other: "Money") -> "Money":
        return Money(money.amount + other.amount)

    @classmethod
    def subtract(cls, money: "Money", other: "Money") -> "Money":
        return Money(money.amount - other.amount)

    @classmethod
    def of(cls, amount: float) -> "Money":
        return Money(amount)

    @classmethod
    def zero(cls) -> "Money":
        return Money.of(0.0)

    def is_positive(self) -> bool:
        return self.amount > 0

    def is_positive_or_zero(self) -> bool:
        return self.amount >= 0

    def negate(self) -> "Money":
        return Money(-self.amount)

    def is_greater_than(self, money: "Money") -> bool:
        return self.amount - money.amount >= 1

    def get_amount(self) -> float:
        return self.amount

    def __repr__(self) -> str:
        return f"${self.amount:.2f}"
