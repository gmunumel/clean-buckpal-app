from src.application.domain.model.money import Money


class WithdrawExceededException(Exception):
    """
    Exception raised when a withdrawal exceeds the available balance.
    This exception is raised when an attempt is made to withdraw
    an amount greater than the available balance in the account.
    """

    def __init__(self, money: Money):
        message = f"Not enough money to withdraw. Tried to transfer {money}!"
        super().__init__(message)
