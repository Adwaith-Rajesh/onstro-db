from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from .utils import create_db_folders
from .utils import dump_cached_schema
from .utils import get_db_path
from .utils import load_cached_schema
from .utils import validate_schema
from onstrodb.errors.schema_errors import SchemaError

# types
DBDataType = Dict[str, Union[int, str, bool]]
SchemaDictType = Dict[str, Dict[str, Union[int, str, bool]]]


class OnstroDb:

    """The main API for the DB"""

    def __init__(self, db_name: str, schema: Optional[SchemaDictType] = None,
                 allow_data_duplication: bool = False) -> None:

        self._db_name = db_name
        self._schema = schema
        self._data_dupe = allow_data_duplication

        # db variables
        self._db: pd.DataFrame = None
        self._modified: bool = False
        self._db_path: str = get_db_path(db_name)

        # validate the user defined schema
        self._validate_schema()

        # start the loading sequence
        self._load_initial_schema()
        self._reload_db()

    def add(self, value: DBDataType) -> str:
        pass

    def add_many(self, values: List[DBDataType]) -> None:
        pass

    def get(self, count: int = 1) -> List[DBDataType]:
        pass

    def get_by_query(self, query: Dict[str, str]) -> List[DBDataType]:
        pass

    def get_by_hash_id(self, hash_id: str) -> DBDataType:
        pass

    def get_all(self) -> List[DBDataType]:
        pass

    def update_by_query(self, query: Dict[str, str], update_data: DBDataType) -> None:
        pass

    def update_by_hash_id(self, hash_id: str, update_data: DBDataType) -> None:
        pass

    def delete_by_query(self, query: Dict[str, str]) -> List[str]:
        pass

    def delete_by_hash_id(self, hash_id: str) -> None:
        pass

    def purge(self) -> None:
        pass

    def _validate_schema(self) -> None:
        if self._schema:
            validate_schema(self._schema)

    def _reload_db(self) -> None:
        """Reload the the pandas DF"""

    def _load_initial_schema(self) -> None:
        """Loads the schema that was provided when the DB was created for the first time"""
        create_db_folders(self._db_path)
        schema = load_cached_schema(self._db_path)
        if schema:
            if self._schema:
                if not schema == self._schema:
                    raise SchemaError(
                        "The schema provided does not match with the initial schema")
            else:
                self._schema = schema.copy()
        else:
            if not self._schema:
                raise SchemaError("The schema is not provided")
            else:
                dump_cached_schema(self._db_path, self._schema)
