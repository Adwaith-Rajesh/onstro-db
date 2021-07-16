import uuid
from pprint import pformat
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from .utils import add_default_to_data
from .utils import create_db_folders
from .utils import dump_cached_schema
from .utils import dump_db
from .utils import generate_hash_id
from .utils import get_db_path
from .utils import load_cached_schema
from .utils import load_db
from .utils import validate_data_with_schema
from .utils import validate_query_data
from .utils import validate_schema
from .utils import validate_update_data
from onstrodb.errors.common_errors import DataDuplicateError
from onstrodb.errors.common_errors import DataError
from onstrodb.errors.schema_errors import SchemaError

# types
DBDataType = Dict[str, object]
SchemaDictType = Dict[str, Dict[str, object]]
GetType = Union[Dict[str, Union[Dict[str, object], str]], None]


class OnstroDb:

    """The main API for the DB"""

    def __init__(self, db_name: str, schema: Optional[SchemaDictType] = None,
                 db_path: Optional[str] = None, allow_data_duplication: bool = False,
                 in_memory: bool = False) -> None:

        self._db_name = db_name
        self._schema = schema
        self._data_dupe = allow_data_duplication
        self._in_memory = in_memory

        # db variables
        self._db: pd.DataFrame = None
        self._db_path: str = get_db_path(db_name)

        if db_path:
            self._db_path = f"{db_path}/{self._db_name}"

        # validate the user defined schema
        self._validate_schema()

        # meta data about the db
        if self._schema:
            self._columns = list(self._schema.keys())

        # start the loading sequence
        self._load_initial_schema()
        self._reload_db()

    def __repr__(self) -> str:
        return pformat(self._to_dict(self._db), indent=4, width=80, sort_dicts=False)

    def __len__(self) -> int:
        return len(self._db.index)

    def add(self, values: List[Dict[str, object]], get_hash_id: bool = False) -> Union[None, List[str]]:
        """Adds a list of values to the DB"""

        new_data: List[Dict[str, object]] = []
        new_hashes: List[str] = []

        for data in values:
            if self._schema:
                if validate_data_with_schema(data, self._schema):
                    data = add_default_to_data(data, self._schema)
                    hash_id = self._get_hash(
                        [str(i) for i in data.values()], list(self._db.index) + new_hashes)
                    new_data.append(data)
                    new_hashes.append(hash_id)

                else:
                    raise DataError(
                        f"The data {data!r} does not comply with the schema")

        new_df = pd.DataFrame(new_data, new_hashes)

        try:
            self._db = pd.concat([self._db, new_df],
                                 verify_integrity=not self._data_dupe)
        except ValueError:
            raise DataDuplicateError(
                "The data provided, contains duplicate values") from None

        if get_hash_id:
            return new_hashes

        return None

    def get_by_query(self, query: Dict[str, object]) -> GetType:
        """Get values from the DB. queries must comply with the schema and must be of length 1"""
        if self._schema:
            if validate_query_data(query, self._schema):
                key = list(query)[0]
                filt = self._db[key] == query[key]
                return self._to_dict(self._db.loc[filt])

        return None

    def get_by_hash_id(self, hash_id: str) -> GetType:
        """Get values from the DB based on their hash ID"""

        if hash_id in self._db.index:
            return self._to_dict(self._db.loc[hash_id])
        return {}

    def get_hash_id(self, condition: Dict[str, object]) -> List[str]:
        """Returns a hash id or a list of ids that matches all the conditions"""

        # the validate_update_method can be used as the same verification style is required here.
        if self._schema:
            if validate_update_data(condition, self._schema):
                return list(self._db.loc[(self._db[list(condition)]
                                          == pd.Series(condition)).all(axis=1)].index)
        return []

    def get_all(self) -> GetType:
        """Return the entire DB in a dict representation"""

        return self._to_dict(self._db)

    def update_by_query(self, query: Dict[str, object], update_data: DBDataType) -> Dict[str, str]:
        """Update the records in the DB with a query"""

        if self._schema:
            if validate_query_data(query, self._schema) and validate_update_data(update_data, self._schema):
                q_key = list(query)[0]
                q_val = query[q_key]

                filt = self._db[q_key] == q_val
                for key, val in update_data.items():
                    self._db.loc[filt, key] = val

                # update the indexes
                indexes = list(self._db.loc[filt].index)
                return self._update_hash_id(indexes)

        return {}

    def update_by_hash_id(self, hash_id: str, update_data: DBDataType) -> Dict[str, str]:
        """Update the records in the DB using their hash id"""

        if hash_id in self._db.index:
            if self._schema:
                if validate_update_data(update_data, self._schema):
                    for key, val in update_data.items():
                        self._db.loc[hash_id, key] = val

                    # update the index
                    return self._update_hash_id([hash_id])

        return {}

    def delete_by_query(self, query: Dict[str, object]) -> None:
        """Delete the records from the db that complies to the query"""

        if self._schema:
            if validate_query_data(query, self._schema):
                key = list(query)[0]
                filt = self._db[key] != query[key]
                self._db = self._db.loc[filt]

    def delete_by_hash_id(self, hash_id: str) -> None:
        """Delete the a records from thr DB based on their hash_id"""

        ids = list(self._db.index)
        if hash_id in ids:
            self._db = self._db.drop(hash_id)

    def raw_db(self) -> pd.DataFrame:
        """Returns the in in memory representation of the DB"""
        return self._db.copy(deep=True)

    def purge(self) -> None:
        """Removes all the data from the runtime instance of the db"""
        self._db = self._db.iloc[0:0]

    def commit(self) -> None:
        """Store the current db in a file"""
        if isinstance(self._db, pd.DataFrame):
            if not self._in_memory:
                dump_db(self._db, self._db_path, self._db_name)

    def _get_hash(self, values: List[str], hash_list: List[str]) -> str:
        """returns the hash id based on the dupe value"""

        def gen_dupe_hash(extra: int = 0) -> str:
            if extra:
                hash_ = generate_hash_id(values + [str(extra)])
            else:
                hash_ = generate_hash_id(values)
            if hash_ in hash_list:
                return gen_dupe_hash(uuid.uuid4().int)
            else:
                return hash_

        if not self._data_dupe:
            return generate_hash_id(values)

        else:
            return gen_dupe_hash()

    def _update_hash_id(self, old_hashes: List[str]) -> Dict[str, str]:
        """Updates the hash when the values are changed"""
        new_hashes: Dict[str, str] = {}
        for idx in old_hashes:
            values = self.get_by_hash_id(idx)

            if isinstance(values, dict):
                hash_ = self._get_hash(
                    list(map(str, values.values())), list(map(str, self._db.index)))

                self._db.rename(index={idx: hash_}, inplace=True)
                new_hashes[idx] = hash_

        return new_hashes

    def _to_dict(self, _df: Union[pd.DataFrame, pd.Series]) -> Dict[str, Union[Dict[str, object], str]]:
        """Returns the dict representation of the DB based on
            the allow_data_duplication value
        """

        if isinstance(_df, pd.DataFrame):
            return _df.to_dict("index")

        else:
            return _df.to_dict()

    def _validate_schema(self) -> None:
        if self._schema:
            validate_schema(self._schema)

    def _reload_db(self) -> None:
        """Reload the the pandas DF"""

        if not self._in_memory:
            data = load_db(self._db_path, self._db_name)
            if isinstance(data, pd.DataFrame):
                self._db = data

            else:
                self._db = pd.DataFrame(columns=self._columns)

        else:
            self._db = pd.DataFrame(columns=self._columns)

    def _load_initial_schema(self) -> None:
        """Loads the schema that was provided when the DB was created for the first time"""
        if not self._in_memory:
            create_db_folders(self._db_path)
        if not self._in_memory:
            schema = load_cached_schema(self._db_path)
        else:
            schema = None
        if schema:
            if self._schema:
                if not schema == self._schema:
                    raise SchemaError(
                        "The schema provided does not match with the initial schema")
            else:
                self._schema = schema.copy()
                self._columns = list(self._schema.keys())
        else:
            if not self._schema:
                raise SchemaError("The schema is not provided")
            else:
                if not self._in_memory:
                    dump_cached_schema(self._db_path, self._schema)
