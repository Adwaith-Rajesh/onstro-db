import os
import pickle
from hashlib import sha256
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

import pandas as pd

from onstrodb.errors.common_errors import DataError
from onstrodb.errors.common_errors import QueryError
from onstrodb.errors.schema_errors import SchemaError

SchemaDictType = Dict[str, Dict[str, object]]


def validate_schema(schema: SchemaDictType) -> bool:
    """Check whether all the keys in schema are valid"""

    valid_field_property_keys = ["type", "required", "default"]

    for key, values in schema.items():
        if not isinstance(key, str):
            raise SchemaError(
                f"The type of the key must be 'str' not {type(key)!r}")

        if "type" not in values:
            raise SchemaError(
                f"The 'type' of the field {key!r} is not defined")

        if values["type"] not in ["int", "str", "bool", "float"]:
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


def validate_query_data(data: Dict[str, object], schema: SchemaDictType) -> bool:
    if len(data) != 1:
        raise QueryError(
            f"The length of the query must be 1 an not {len(data)!r}")

    if not all(i in schema for i in data.keys()):
        raise QueryError("Unknown key found in query")

    key = list(data)[0]

    if type(data[key]).__name__ != schema[key]["type"]:
        raise QueryError(
            f"The type of {key!r} must be {schema[key]['type']!r}")

    return True


def validate_update_data(data: Dict[str, object], schema: SchemaDictType) -> bool:
    if not all(i in schema for i in data.keys()):
        raise DataError("Unknown key found in data")

    key = list(data)

    for k in key:
        if type(data[k]).__name__ != schema[k]["type"]:
            raise DataError(
                f"The type of {k!r} must be {schema[k]['type']!r}")

    return True


def add_default_to_data(data: Dict[str, object], schema: SchemaDictType) -> Dict[str, object]:
    """Adds the default values present in the schema to the required fields
        if the values are not provided in the data
    """

    # add non as defaults to the field that is not required and does not have
    # a default value
    non_default_values = [i for i in schema if all(
        j not in schema[i] for j in ["required", "default"])]

    for val in non_default_values:
        schema[val]["default"] = None

    defaults: List[str] = [j for j in [
        i for i in schema if "default" in schema[i]] if "default" in schema[j]]

    if not all(i in data for i in defaults):
        for i in defaults:
            if i not in data:
                data[i] = schema[i]["default"]

        return data

    else:
        return data


def dump_db(df: pd.DataFrame, db_path: str, db_name: str) -> None:
    """Converts the df to a pickle file"""
    df.to_pickle(os.path.join(db_path, f"{db_name}.db"))


def load_db(db_path: str, db_name: str) -> Union[pd.DataFrame, None]:
    """loads the df from the pickle file"""
    path = os.path.join(db_path, f"{db_name}.db")
    if Path(path).is_file():
        return pd.read_pickle(path)

    else:
        return None


def get_db_path(db_name: str) -> str:
    """returns the absolute path of the DB"""
    # default = os.path.join(os.path.expanduser("~"), ".cache", "onstrodb")
    default = os.path.join(".", "onstro-db")
    db_directory = os.environ.get("ONSTRO_DB_PATH", default=default)

    return os.path.join(db_directory, db_name)


def create_db_folders(db_path: str) -> None:
    path = Path(db_path)
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)


def load_cached_schema(db_path: str) -> Union[SchemaDictType, None]:
    """Loads the existing schema, that was provided when the DB was created for the first time."""
    c_schema_path = os.path.join(db_path, "db.schema")

    if Path(c_schema_path).is_file():
        with open(c_schema_path, "rb") as f:
            return pickle.load(f)
    else:
        return None


def dump_cached_schema(db_path: str, schema: SchemaDictType) -> None:
    """Dumps the schema in a pickle form for later use"""
    c_schema_path = os.path.join(db_path, "db.schema")

    with open(c_schema_path, "wb") as f:
        pickle.dump(schema, f)


def generate_hash_id(values: List[str]) -> str:
    """Genetate SHA256 check sum by combining all the entries inside the values list,
        and return the first 8 characters.
    """
    return sha256(bytes("".join(values), encoding="utf-8")).hexdigest()[:8]
