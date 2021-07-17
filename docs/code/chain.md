<h1 align="center"> Onstro DB </h1>

## Multiple conditions in queries

As you might have noticed that all the methods that accept query as an argument, the query can only be one condition long.
In order have queries that have multiple condition you can use that following technique

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

hid = db.get_hash_id({"name": "ad", "age": 3})
db.update_by_hash_id(hid[0], {"name": 'mike'})

print(db)
```

    {   '7b672af4': {'name': 'ad', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        'f3d32e1e': {'name': 'dev', 'age': 3}}

    {   '110f1f27': {'name': 'mike', 'age': 3},
        '93b626d2': {'name': 'fred', 'age': 4},
        'f3d32e1e': {'name': 'dev', 'age': 3}}

> The `get_hash_id` method returns a list of all the hash ids of rows that matches all the conditions provided in the query.
