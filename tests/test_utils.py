from typing import Dict
from typing import Union

import pytest

from onstrodb.core.utils import generate_hash_id
from onstrodb.core.utils import validate_data_with_schema
from onstrodb.core.utils import validate_schema
from onstrodb.errors.schema_errors import SchemaError


test_schema: Dict[str, Dict[str, Union[int, str, bool]]] = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int", "required": True},
    "place": {"type": "str", "default": "canada"}
}


@pytest.mark.parametrize(
    "test_input,output",
    [
        (["Hello", "World"], "872e4e50"),
        (["ad", "4", "high school"], "1199e3f8"),
        (["python", "test", "param", "3"], "411996b0")
    ]
)
def test_generate_hash_id(test_input, output):
    assert generate_hash_id(test_input) == output


@pytest.mark.parametrize(
    "test_input,output",
    [
        ({"name": {"type": "str", "required": True, "default": "ad"}}, True),
        ({"name": {"type": "str"}, "age": {"type": "int"}}, True)
    ]
)
def test_validate_schema_accepted_conditions(test_input, output):
    assert validate_schema(test_input) is output


@pytest.mark.parametrize(
    "test_schema",
    [
        {1: {"type": "int"}},
        {"name": {"type": "str", "default": 12}},
        {"name": {"default": "fr"}},
        {"name": {"type": "str", "required": 3}},
        {"name": {"type": str}}
    ]
)
def test_validate_schema_error_conditions(test_schema):
    with pytest.raises(SchemaError):
        _ = validate_schema(test_schema)


@pytest.mark.parametrize(
    "test_input,output",
    [
        ({"name": "ad", "age": 3, "place": "texas"}, True),
        ({"name": "ad", "age": 3}, True),
        ({"name": "ad"}, False),
        ({"name": "ad", "place": "texas"}, False),
        ({"name": "ad", "age": "test"}, False),
        ({"name": "ad", "age": 12, "place": 3}, False)
    ]
)
def test_validate_data_with_schema(test_input, output):
    assert validate_data_with_schema(test_input, test_schema) == output
