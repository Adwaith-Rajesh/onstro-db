import os
import shutil
from pathlib import Path
from typing import Dict

import pytest

from onstrodb.core.db import OnstroDb
from onstrodb.core.utils import create_db_folders
from onstrodb.core.utils import dump_cached_schema
from onstrodb.core.utils import generate_hash_id
from onstrodb.errors.common_errors import DataDuplicateError
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
def db_class():
    yield OnstroDb(db_name="test", db_path="./test_onstro", schema=test_schema)
    remove_folders()


@pytest.fixture
def rm_folder():
    yield
    remove_folders()


def test_file_folder_creation(db_class):
    assert Path("./test_onstro").is_dir() is True
    assert Path("./test_onstro/test").is_dir() is True
    assert Path("./test_onstro/test/db.schema").is_file() is True


@pytest.mark.usefixtures("rm_folder")
def test_schema_loading():
    create_db_folders("./test_onstro/test")
    dump_cached_schema(schema=test_schema, db_path="./test_onstro/test")
    db_class = OnstroDb(db_name="test", db_path="./test_onstro")
    assert db_class._schema == test_schema


@pytest.mark.usefixtures("rm_folder")
def test_db_schema_error_schema_not_provided():
    with pytest.raises(SchemaError):
        _ = OnstroDb(db_name="test", db_path="test_onstro")


@pytest.mark.usefixtures("rm_folder")
def test_db_schema_error_schema_mismatch():
    create_db_folders("./test_onstro/test")
    dump_cached_schema(schema=test_schema, db_path="./test_onstro/test")

    new_schema: Dict[str, Dict[str, object]] = {
        "name": {"type": "str", "required": True},
        "age": {"type": "int"}
    }

    with pytest.raises(SchemaError):
        _ = OnstroDb(db_name="test", db_path="test_onstro", schema=new_schema)


@pytest.mark.usefixtures("rm_folder")
def test_db_add():
    db = OnstroDb(db_name="test", db_path="test_onstro", schema=test_schema)
    db.add([
        {"name": "ad",
         "age": 34,
         "place": "texas"}
    ])

    assert db._db.to_dict() == {'name': {'ec676189': 'ad'}, 'age': {
        'ec676189': 34}, 'place': {'ec676189': 'texas'}}


@pytest.mark.usefixtures("rm_folder")
def test_add_with_return_values():

    data1 = {
        "name": "ad",
        "age": 34,
        "place": "texas"
    }
    data2 = {
        "name": "test",
        "age": 35,
        "place": "vegas"
    }
    db = OnstroDb(db_name="test", db_path="test_onstro", schema=test_schema)
    ids = db.add([data1, data2], get_hash_id=True)

    assert ids == [generate_hash_id([str(i) for i in data1.values()]), generate_hash_id([
        str(i) for i in data2.values()])]


@pytest.mark.usefixtures("rm_folder")
def test_db_commit():
    db = OnstroDb(db_name="test", db_path="test_onstro", schema=test_schema)
    db.add([
        {"name": "ad",
         "age": 34,
         "place": "texas"}
    ])
    db.commit()

    assert Path(os.path.join("test_onstro", "test",
                "test.db")).is_file() is True


@pytest.mark.usefixtures("rm_folder")
def test_db_purge():
    db = OnstroDb(db_name="test", db_path="test_onstro", schema=test_schema)
    db.add([
        {"name": "ad",
         "age": 34,
         "place": "texas"}
    ])

    assert len(db._db) == 1
    db.purge()
    assert db._db.empty is True


@pytest.mark.usefixtures("rm_folder")
def test_db_add_raises_dupe_error():

    db = OnstroDb(db_name="test", db_path="test_onstro", schema=test_schema)

    with pytest.raises(DataDuplicateError):
        db.add([
            {"name": "ad", "age": 3, "place": "canada"},
            {"name": "ad", "age": 3, "place": "canada"},
        ])


def test_db_in_memory():

    db = OnstroDb(db_name="test", schema=test_schema,
                  in_memory=True, db_path="test_onstro")
    db.add([
        {"name": "test", "age": 4}
    ])

    assert Path("test_onstro").is_dir() is False


@pytest.mark.parametrize(
    "test_input,output",
    (
        ({"age": 3},  {'a811ebf6': {'name': 'ab', 'age': 3, 'place': 'canada'},
                       'a103f392': {'name': 'ac', 'age': 3, 'place': 'france'}}),
        ({"name": "ac"}, {'a103f392': {
            'name': 'ac', 'age': 3, 'place': 'france'}}),
        ({"place": "france"}, {'a103f392': {
            'name': 'ac', 'age': 3, 'place': 'france'}}),
        ({"age": 5}, {})
    )
)
def test_db_get_by_query_no_dupe(test_input, output):

    db = OnstroDb(db_name="test", in_memory=True, schema=test_schema)
    db.add([
        {"name": "ab", "age": 3},
        {"name": "ac", "age": 3, "place": "france"},
        {"name": "ad", "age": 4}
    ])

    assert db.get_by_query(test_input) == output


@pytest.mark.parametrize(
    "test_input",
    (
        {"name": "test", "age": 3},
        {"Name": "hello"},
        {"age": "3"}
    )
)
def test_db_get_by_query_failure(test_input):
    db = OnstroDb(db_name="test", in_memory=True, schema=test_schema)
    with pytest.raises(QueryError):
        db.get_by_query(test_input)


def test_db_get_all_no_dupe():
    db = OnstroDb(db_name="test", in_memory=True,
                  schema=test_schema, allow_data_duplication=False)
    db.add([
        {"name": "ab", "age": 3},
        {"name": "ac", "age": 3, "place": "france"},
        {"name": "ad", "age": 4}
    ])

    assert db.get_all() == {'a811ebf6': {'name': 'ab', 'age': 3, 'place': 'canada'},
                            'a103f392': {'name': 'ac', 'age': 3, 'place': 'france'},
                            'e160bb9c': {'name': 'ad', 'age': 4, 'place': 'canada'}}


def test_db_get_all_dupe():
    db = OnstroDb(db_name="test", in_memory=True,
                  schema=test_schema, allow_data_duplication=True)
    db.add([
        {"name": "ab", "age": 3},
        {"name": "ac", "age": 3, "place": "france"},
        {"name": "ad", "age": 4}
    ])

    assert db.get_all() == {'a103f392': {'age': 3, 'name': 'ac', 'place': 'france'},
                            'a811ebf6': {'age': 3, 'name': 'ab', 'place': 'canada'},
                            'e160bb9c': {'age': 4, 'name': 'ad', 'place': 'canada'}}


def test_db_delete_by_query():
    db = OnstroDb(db_name="test", in_memory=True,
                  schema=test_schema, allow_data_duplication=False)
    db.add([
        {"name": "ab", "age": 3},
        {"name": "ac", "age": 3, "place": "france"},
        {"name": "ad", "age": 4}
    ])

    assert db.get_all() == {'a811ebf6': {'name': 'ab', 'age': 3, 'place': 'canada'},
                            'a103f392': {'name': 'ac', 'age': 3, 'place': 'france'},
                            'e160bb9c': {'name': 'ad', 'age': 4, 'place': 'canada'}}

    db.delete_by_query({"age": 3})

    assert db.get_all() == {'e160bb9c': {'name': 'ad',
                                         'age': 4, 'place': 'canada'}}


@pytest.mark.parametrize(
    "hash_id,output",
    (
        ('a811ebf6', {'a103f392': {'age': 3, 'name': 'ac', 'place': 'france'},
                      'e160bb9c': {'age': 4, 'name': 'ad', 'place': 'canada'}}),

        ('a103f392', {'a811ebf6': {'age': 3, 'name': 'ab', 'place': 'canada'},
                      'e160bb9c': {'age': 4, 'name': 'ad', 'place': 'canada'}}),

        ('e160bb9c', {'a103f392': {'age': 3, 'name': 'ac', 'place': 'france'},
                      'a811ebf6': {'age': 3, 'name': 'ab', 'place': 'canada'}})
    )
)
def test_db_delete_by_hash_id(hash_id, output):
    db = OnstroDb(db_name="test", in_memory=True,
                  schema=test_schema, allow_data_duplication=False)
    db.add([
        {"name": "ab", "age": 3},
        {"name": "ac", "age": 3, "place": "france"},
        {"name": "ad", "age": 4}
    ])

    db.delete_by_hash_id(hash_id)
    assert db.get_all() == output


@pytest.mark.parametrize(
    "query,ud,output",
    (
        ({"name": "ab"}, {"name": "adw", "age": 4}, {'f350b1aa': {'name': 'adw', 'age': 4, 'place': 'canada'},
                                                     'a103f392': {'name': 'ac', 'age': 3, 'place': 'france'},
                                                     'e160bb9c': {'name': 'ad', 'age': 4, 'place': 'canada'}}),

        ({"name": "ac"}, {"place": "denmark"}, {'a811ebf6': {'name': 'ab', 'age': 3, 'place': 'canada'},
                                                'f6e44b0a': {'name': 'ac', 'age': 3, 'place': 'denmark'},
                                                'e160bb9c': {'name': 'ad', 'age': 4, 'place': 'canada'}}),

        ({"name": "az"}, {"place": "denmark"}, {'a811ebf6': {'name': 'ab', 'age': 3, 'place': 'canada'},
                                                'a103f392': {'name': 'ac', 'age': 3, 'place': 'france'},
                                                'e160bb9c': {'name': 'ad', 'age': 4, 'place': 'canada'}})
    )
)
def test_db_update_by_query(query, ud, output):
    db = OnstroDb(db_name="test", in_memory=True,
                  schema=test_schema, allow_data_duplication=False)
    db.add([
        {"name": "ab", "age": 3},
        {"name": "ac", "age": 3, "place": "france"},
        {"name": "ad", "age": 4}])

    db.update_by_query(query, ud)
    assert db.get_all() == output


@pytest.mark.parametrize(
    "hash_id,ud,output",
    (
        ("a811ebf6", {"name": "adw", "age": 4}, {'f350b1aa': {'name': 'adw', 'age': 4, 'place': 'canada'},
                                                 'a103f392': {'name': 'ac', 'age': 3, 'place': 'france'},
                                                 'e160bb9c': {'name': 'ad', 'age': 4, 'place': 'canada'}}),

        ("a103f392", {"place": "denmark"}, {'a811ebf6': {'name': 'ab', 'age': 3, 'place': 'canada'},
                                            'f6e44b0a': {'name': 'ac', 'age': 3, 'place': 'denmark'},
                                            'e160bb9c': {'name': 'ad', 'age': 4, 'place': 'canada'}}),

        ("a103f394", {"place": "denmark"}, {'a811ebf6': {'name': 'ab', 'age': 3, 'place': 'canada'},
                                            'a103f392': {'name': 'ac', 'age': 3, 'place': 'france'},
                                            'e160bb9c': {'name': 'ad', 'age': 4, 'place': 'canada'}})
    )
)
def test_db_update_hash_id(hash_id, ud, output):
    db = OnstroDb(db_name="test", in_memory=True,
                  schema=test_schema, allow_data_duplication=False)
    db.add([
        {"name": "ab", "age": 3},
        {"name": "ac", "age": 3, "place": "france"},
        {"name": "ad", "age": 4}])

    db.update_by_hash_id(hash_id, ud)
    assert db.get_all() == output
