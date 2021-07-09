class PropertyValueError(Exception):
    """Custom error raised when the type of a property is invalid"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class SchemaValueError(Exception):
    """Error raised when the values in the schema provided by the user has issue"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
