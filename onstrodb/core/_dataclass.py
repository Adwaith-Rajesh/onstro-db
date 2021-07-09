from typing import Any
from typing import Dict
from typing import Generic
from typing import Literal
from typing import Optional
from typing import TypeVar
from typing import Union

import pydantic

from onstrodb.errors.schema_errors import PropertyValueError

TDefault = TypeVar("TDefault", int, str, bool)


class Property(pydantic.BaseModel, Generic[TDefault]):

    """The property of column in the DB"""

    property_type: Literal["str", "int", "bool"]
    default: Optional[TDefault]
    required: Optional[bool]

    @pydantic.validator("default")
    @classmethod
    def validate_default(cls, value: Any, values: Dict[str, Union[str, TDefault, None]]) -> Union[None, TDefault]:
        """Check whether default values is the same type as the property type"""
        if value.__class__.__name__ != values["property_type"]:
            raise PropertyValueError(
                message="type of default should be the same as mentioned in 'property_type'")

        return value
