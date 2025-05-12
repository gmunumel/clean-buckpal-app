class ValidationException(Exception):
    """
    Exception raised for validation errors in the application.
    This exception is used to indicate that a validation error has occurred
    during the processing of a request or operation.
    """

    def __init__(self, status_code: int, message: str):
        super().__init__(status_code, message)
