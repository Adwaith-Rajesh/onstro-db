import shutil
from pathlib import Path
from typing import Dict

import pytest

from onstrodb.core.db import OnstroDb
from onstrodb.core.utils import create_db_folders
from onstrodb.core.utils import dump_cached_schema
from onstrodb.errors.schema_errors import SchemaError


test_schema: Dict[str, Dict[str, object]] = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int", "required": True},
    "place": {"type": "str", "default": "canada"}
}


def remove_folders():
    "removes the test folders"
    shutil.rmtree('./test_onstro')


@ pytest.fixture
def db_class():
    yield OnstroDb(db_name="test", db_path="./test_onstro", schema=test_schema)
    remove_folders()


@ pytest.fixture
def rm_folder():
    yield
    remove_folders()


def test_file_folder_creation(db_class):
    assert Path("./test_onstro").is_dir() is True
    assert Path("./test_onstro/test").is_dir() is True
    assert Path("./test_onstro/test/db.schema").is_file() is True


@ pytest.mark.usefixtures("rm_folder")
def test_schema_loading():
    create_db_folders("./test_onstro/test")
    dump_cached_schema(schema=test_schema, db_path="./test_onstro/test")
    db_class = OnstroDb(db_name="test", db_path="./test_onstro")
    assert db_class._schema == test_schema


@ pytest.mark.usefixtures("rm_folder")
def test_db_schema_error_schema_not_provided():
    with pytest.raises(SchemaError):
        _ = OnstroDb(db_name="test", db_path="test_onstro")


@ pytest.mark.usefixtures("rm_folder")
def test_db_schema_error_schema_mismatch():
    create_db_folders("./test_onstro/test")
    dump_cached_schema(schema=test_schema, db_path="./test_onstro/test")

    new_schema: Dict[str, Dict[str, object]] = {
        "name": {"type": "str", "required": True},
        "age": {"type": "int"}
    }

    with pytest.raises(SchemaError):
        _ = OnstroDb(db_name="test", db_path="test_onstro", schema=new_schema)
