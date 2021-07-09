# all the test related to the DB schema and its related classes
import pytest
from pydantic.error_wrappers import ValidationError

from onstrodb.core._dataclass import Property
from onstrodb.errors.schema_errors import PropertyValueError


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
