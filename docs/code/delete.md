## Deleting data from the DB

There are three ways to delete data from a DB

- delete_by_query
- delete_by_hash_id
- purge

### delete_by_query

The `delete_by_query` accepts a single condition which removes all the rows that mathes that condition

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
    {"name": "dev", "age": 5}
])

print(db)

db.delete_by_query({"name": "ad"})  # queries can only be one condition long(There is a work around for this)

print(db)
```

    {   '7b672af4': {'name': 'ad', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        '41907268': {'name': 'dev', 'age': 5}}
    {'93b626d2': {'name': 'fred', 'age': 4}, '41907268': {'name': 'dev', 'age': 5}}

### delete_by_hash_id

The `delete_by_hash_id` taskes the hash id of the row as an argument

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
    {"name": "dev", "age": 5}
])

print(db)

db.delete_by_hash_id("93b626d2")

print(db)
```

    {   '7b672af4': {'name': 'ad', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        '41907268': {'name': 'dev', 'age': 5}}
    {'7b672af4': {'name': 'ad', 'age': 3}, '41907268': {'name': 'dev', 'age': 5}}

### purge

Purging a DB will delete all the rows.

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
    {"name": "dev", "age": 5}
])

print(db)

db.purge()
db.commit()  # to save the changes

print(db)
```

    {   '7b672af4': {'name': 'ad', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        '41907268': {'name': 'dev', 'age': 5}}

    {}
