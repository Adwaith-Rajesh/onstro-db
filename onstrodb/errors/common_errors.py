class DataError(Exception):
    """Raised when the data provided by the user have conflits with the schema
        or the data is someways invalid
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DataDuplicateError(Exception):
    """Raised when the user provided already exists in DB"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class QueryError(Exception):
    """Raised when the query used by the user to access data / update data
        is invalid
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
