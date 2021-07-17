<h1 align="center"> Onstro DB </h1>

## Getting data from the DB

You can get data from a DB with the following methods

- get_by_query()
- get_by_hash_id()
- get_all()

### get_by_query

The `get_by_query` method takes a single condition query and return a dict of all the rows that matches that condition

```python
from onstrodb import OnstroDb

schema = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int"}
}

db = OnstroDb(db_name="test", schema=schema)

db.add([
    {"name": "ad", "age": 3},
    {"name": "fred", "age": 4},
    {"name": "dev", "age": 3}
])

data = db.get_by_query({"age": 3})  # queries can only be one condition long(There is a work around for this)

print(data)
```

    {'7b672af4': {'name': 'ad', 'age': 3}, 'f3d32e1e': {'name': 'dev', 'age': 3}}

### get_by_hash_id

The `get_by_hash_id` accepts the hash id of the row that you want to get as an argument.

```python
from onstrodb import OnstroDb

schema = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int"}
}

db = OnstroDb(db_name="test", schema=schema)

db.add([
    {"name": "ad", "age": 3},
    {"name": "fred", "age": 4},
    {"name": "dev", "age": 3}
])

print(db)

data = db.get_by_hash_id("7b672af4")

print(data)
```

    {   '7b672af4': {'name': 'ad', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        'f3d32e1e': {'name': 'dev', 'age': 3}}
    {'name': 'ad', 'age': 3}

### get_all

The `get_all` methods returns all the rows in the DB

```python
from onstrodb import OnstroDb

schema = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int"}
}

db = OnstroDb(db_name="test", schema=schema)

db.add([
    {"name": "ad", "age": 3},
    {"name": "fred", "age": 4},
    {"name": "dev", "age": 3}
])

data = db.get_all()

print(data)
```

    {'7b672af4': {'name': 'ad', 'age': 3}, '93b626d2': {'name': 'fred', 'age': 4}, 'f3d32e1e': {'name': 'dev', 'age': 3}}

```python

```
