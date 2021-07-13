import shutil
from typing import Dict

import pytest

from onstrodb.core.utils import add_default_to_data
from onstrodb.core.utils import generate_hash_id
from onstrodb.core.utils import validate_data_with_schema
from onstrodb.core.utils import validate_query_data
from onstrodb.core.utils import validate_schema
from onstrodb.errors.common_errors import QueryError
from onstrodb.errors.schema_errors import SchemaError


test_schema: Dict[str, Dict[str, object]] = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int", "required": True},
    "place": {"type": "str", "default": "canada"}
}


def remove_folders():
    "removes the test folders"
    shutil.rmtree('./test_onstro')


@pytest.fixture
def rm_folder():
    yield
    remove_folders()


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
        ({"name": {"type": "str"}, "age": {"type": "int"}}, True),
        ({"name": {"type": "str"}, "age": {"type": "float"}}, True)
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


@pytest.mark.parametrize(
    "test_input,output",
    [
        ({"name": "Mike", "age": 24, "place": "denmark", "exp": 3.4},
         {"name": "Mike", "age": 24, "place": "denmark", "exp": 3.4}),

        ({"name": "ad", "age": 23},
         {"name": "ad", "age": 23, "place": "canada", "exp": None}),

        ({"name": "Hello", "age": 24}, {
         "name": "Hello", "age": 24, "place": "canada", "exp": None}),

        ({"name": "ad", "age": 23, "place": "texas", "exp": 3.4},
         {"name": "ad", "age": 23, "place": "texas", "exp": 3.4})
    ]
)
def test_add_default_to_data(test_input, output):
    test_schema: Dict[str, Dict[str, object]] = {
        "name": {"type": "str", "required": True},
        "age": {"type": "int", "required": True},
        "place": {"type": "str", "default": "canada"},
        "exp": {"type": "float"}
    }
    assert add_default_to_data(test_input, test_schema) == output


@pytest.mark.parametrize(
    "test_input,output",
    (
        ({"name": "test"}, True),
        ({"age": 3}, True),
        ({"place": "canada"}, True)
    )
)
def test_validate_query_data_accpected_conditions(test_input, output):
    assert validate_query_data(test_input, test_schema) is output


@pytest.mark.parametrize(
    "test_input",
    (
        {"name": "test", "age": 3},
        {"Name": "hello"},
        {"age": "3"}
    )
)
def test_validate_query_data_error_condition(test_input):
    with pytest.raises(QueryError):
        validate_query_data(test_input, test_schema)
