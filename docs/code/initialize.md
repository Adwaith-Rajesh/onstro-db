<h1 align="center"> Onstro DB </h1>

### Initializing the DB

```python
from onstrodb import OnstroDb

schema = {
    "name": {"type": "str"}
}


db = OnstroDb(db_name="test", db_path="./test_db", schema=schema)
```

The above code snippet will create a new DB with the name `test` in the directory `test_db`. The tree structure of the directory will look something like this.

```commandline
`-- test_db
    `-- test
        |-- db.schema
        `-- test.db
```

The `db.schema` file stores the initially provided schema, thus avoiding the need to provide the schema during the second run.

> The supported types for the schema are **int**, **str**, **bool**, **float**. and these must be in quotes.

> if **db_path** is not provided then it will default to `./onstro-db`

---

### In memory DB

To make an in memory DB, Initialize the DB as follows.

```python
from onstrodb import OnstroDb

schema = {
    "name": {"type": "str"}
}

db = OnstroDb(db_name="test", schema=schema, in_memory=True)

```

This will not create the files as shown in the above snippet.

---

### Allowing duplicate values.

The DB is designed not to have duplicate values, and if tried to insert one, will raise an error.

In order to handle duplicate values initialize the DB as follows.

```python

from onstrodb import OnstroDb

schema = {
    "name": {"type": "str"}
}

db = OnstroDb(db_name="test", schema=schema, allow_duplicate_values=True)

```

This will work with both normal and in memory DB.

---
