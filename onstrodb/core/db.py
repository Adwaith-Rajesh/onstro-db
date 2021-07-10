from typing import Dict
from typing import List
from typing import Union

import pandas as pd  # noqa: F401


DBDataType = Dict[str, Union[int, str, bool]]


class OnstroDb():

    def __init__(self, db_name: str, allow_data_duplication: bool = False) -> None:
        pass

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
