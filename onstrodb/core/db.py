from typing import Dict
from typing import List
from typing import Union

import pandas as pd

DBDataType = Dict[str, Union[int, str, bool]]
SchemaDictType = Dict[str, Dict[str, object]]


class OnstroDb:

    """The main API for the DB"""

    def __init__(self, db_name: str, schema: SchemaDictType, allow_data_duplication: bool = False) -> None:

        self._db_name = db_name
        self._schema = schema
        self._data_dupe = allow_data_duplication

        self._db: pd.DataFrame = None
        self._modified: bool = False

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

    def _reload_db(self) -> None:
        """Reload the the pandas DF"""
