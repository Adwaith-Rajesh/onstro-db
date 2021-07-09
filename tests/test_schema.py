# all the test related to the DB schema and its related classes
from typing import Any
from typing import Dict

import pytest
from pydantic.error_wrappers import ValidationError

from onstrodb.core._dataclass import Property
from onstrodb.core.utils import validate_convert_schema
from onstrodb.errors.schema_errors import PropertyValueError
from onstrodb.errors.schema_errors import SchemaValueError


def test_property():
    tp = Property(property_type="int", required=True, default=10)
    assert tp.property_type == "int"
    assert tp.required is True
    assert tp.default == 10


def test_property_validation_error():
    with pytest.raises(ValidationError):
        _ = Property(property_type="list", required=False)


def test_property_default_type_error():
    with pytest.raises(PropertyValueError):
        Property(property_type="int", default="s")


def test_schema_to_property_schema_convertion():
    test_schema: Dict[str, Dict[str, Any]] = {
        "name": {"property_type": "str", "required": True},
        "age": {"property_type": "int", "required": False},
        "place": {"property_type": "str", "default": "canada"}
    }

    schema = validate_convert_schema(test_schema)
    assert len(schema) == 3
    assert schema["name"].property_type == "str"
    assert schema["name"].required is True
    assert schema["age"].property_type == "int"
    assert schema["age"].required is False
    assert schema["place"].property_type == "str"
    assert schema["place"].default == "canada"
    assert schema["place"].required is None


def test_schema_to_property_schema_exception():
    test_schema = {
        "name": {"property_type": "str", "required": True},
        "age": {"property_type": "int", "required": False},
        "place": {"property_type": "str", "default": 2}
    }
    with pytest.raises(SchemaValueError):
        _ = validate_convert_schema(test_schema)
