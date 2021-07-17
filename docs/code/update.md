<h1 align="center"> Onstro DB </h1>

## Updating values in the DB

The values in the DB can be updated using the following methods

- update_by_query()
- update_by_hash_id()

### update_by_query

The `update_by_query` method accept the query as the first arguments the data to update to as the second. Its returns a dict of all the hash ids that got updated.

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
ids = db.update_by_query({"age": 4}, {"name": "adrian"})
print(db)

print("The changed indexes: ", ids)

```

    {   '7b672af4': {'name': 'ad', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        'f3d32e1e': {'name': 'dev', 'age': 3}}

    {   '7b672af4': {'name': 'ad', 'age': 3},
        '14c967a9': {'name': 'adrian', 'age': 4},
        'f3d32e1e': {'name': 'dev', 'age': 3}}

    The changed indexes:  {'93b626d2': '14c967a9'}

### update_by_hash_id

The `update_by_hash_id` takes the hash id of the row as the first argument and data to update to as the second

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
ids = db.update_by_hash_id("7b672af4", {"name": "mike"})
print(db)
print("The changed indexes: ", ids)
```

    {   '7b672af4': {'name': 'ad', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        'f3d32e1e': {'name': 'dev', 'age': 3}}

    {   '110f1f27': {'name': 'mike', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        'f3d32e1e': {'name': 'dev', 'age': 3}}

    The changed indexes:  {'7b672af4': '110f1f27'}
