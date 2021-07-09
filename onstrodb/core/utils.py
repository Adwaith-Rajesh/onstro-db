from typing import Any
from typing import Dict

from ._dataclass import Property
from onstrodb.errors.schema_errors import PropertyValueError
from onstrodb.errors.schema_errors import SchemaValueError


def validate_convert_schema(schema: Dict[str, Dict[str, object]]) -> Dict[str, Property[Any]]:
    """Converts the user provided schema to a str -> Property schema
    """
    try:
        return {key: Property(**value) for key, value in schema.items()}
    except PropertyValueError:
        raise SchemaValueError(message="The values passed in the schema are not valid. Possible that the type of 'default' value \
        may not match the 'property_type'")
