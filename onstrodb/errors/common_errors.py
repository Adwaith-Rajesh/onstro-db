class DataError(Exception):
    """Raised when the data provided by the user have conflits with the schema
        or the data is someways invalid
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
