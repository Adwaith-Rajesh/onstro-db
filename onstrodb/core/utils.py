from hashlib import sha256
from typing import Any
from typing import Dict
from typing import List

from ._dataclass import Property
from onstrodb.errors.schema_errors import PropertyValueError
from onstrodb.errors.schema_errors import SchemaValueError

SchemaDictType = Dict[str, Dict[str, object]]


def validate_convert_schema(schema: SchemaDictType) -> Dict[str, Property[Any]]:
    """Converts the user provided schema to a str -> Property schema
    """
    try:
        return {key: Property(**value) for key, value in schema.items()}
    except PropertyValueError:
        raise SchemaValueError(message="The values passed in the schema are not valid. Possible that the type of 'default' value \
        may not match the 'property_type'")


def cross_validate_with_db(test_schema: SchemaDictType, schema: SchemaDictType) -> bool:
    pass


def generate_hash_id(values: List[str]) -> str:
    """Genetate SHA256 check sum by combining all the entries inside the values list,
        and return the first 8 characters.
    """
    return sha256(bytes("".join(values), encoding="utf-8")).hexdigest()[:8]
