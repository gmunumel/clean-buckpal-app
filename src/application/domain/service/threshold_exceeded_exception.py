from src.application.domain.model.money import Money


class ThresholdExceededException(Exception):
    """
    Exception raised when a transfer exceeds the maximum threshold.
    This exception is raised when an attempt is made to transfer
    an amount greater than the maximum threshold for transferring money.
    Attributes:
        threshold (Money): The maximum threshold for transferring money.
        actual (Money): The actual amount attempted to be transferred.
    """

    def __init__(self, threshold: Money, actual: Money):
        message = (
            f"Maximum threshold for transferring money exceeded. "
            f"Tried to transfer {actual}, but threshold is {threshold}!"
        )
        super().__init__(message)
