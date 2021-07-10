import os
from hashlib import sha256
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from onstrodb.errors.schema_errors import SchemaError

SchemaDictUnknownType = Dict[str, Dict[str, object]]
SchemaDictType = Dict[str, Dict[str, Union[int, str, bool]]]


def validate_schema(schema: SchemaDictUnknownType) -> bool:
    """Check whether all the keys in schema are valid"""

    valid_field_property_keys = ["type", "required", "default"]

    for key, values in schema.items():
        if not isinstance(key, str):
            raise SchemaError(
                f"The type of the key must be 'str' not {type(key)!r}")

        if "type" not in values:
            raise SchemaError(
                f"The 'type' of the field {key!r} is not defined")

        if values["type"] not in ["int", "str", "bool"]:
            raise SchemaError(
                "The value of 'type' must be any of ('int', 'str', 'bool') with quotes.")

        if not all([i in valid_field_property_keys for i in values]):
            raise SchemaError(
                f"The field properties must only include {valid_field_property_keys!r}")

        if "default" in values:
            if type(values["default"]).__name__ != values["type"]:
                raise SchemaError(
                    f"The type of 'default' must be {values['type']!r} for the field {key!r}")

        if "required" in values:
            if not isinstance(values["required"], bool):
                raise SchemaError(
                    f"The type of 'required' must be 'bool' not {type(values['required']).__name__!r}")

    return True


def validate_data_with_schema(data: Dict[str, object], schema: SchemaDictType) -> bool:
    """Check whether the data complies with the schema"""

    # check whether all the keys are present in the schema
    if not all(i in schema.keys() for i in data.keys()):
        return False

    # check whether the "required" values are inside the data
    required: List[str] = [j for j in [
        i for i in schema if "required" in schema[i]] if schema[j]["required"]]
    for r in required:
        if r not in data:
            return False

    # verify the type of all the data
    for d in data:
        if type(data[d]).__name__ != schema[d]["type"]:
            return False

    return True


def get_db_path(db_name: str) -> str:
    """returns the absolute path of the DB"""
    default = os.path.join(os.path.expanduser("~"), ".cache", "onstrodb")
    db_directory = os.environ.get("ONSTRO_DB_PATH", default=default)

    return os.path.join(db_directory, db_name)


def create_db_folders_files(db_path: str) -> None:
    path = Path(db_path)
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)


def generate_hash_id(values: List[str]) -> str:
    """Genetate SHA256 check sum by combining all the entries inside the values list,
        and return the first 8 characters.
    """
    return sha256(bytes("".join(values), encoding="utf-8")).hexdigest()[:8]
