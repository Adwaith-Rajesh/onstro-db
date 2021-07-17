<h1 align="center"> Onstro DB </h1>

## Adding Data

Values can be added to the DB with the `.add()` method. It takes a list of values to add to the DB.

```python
from onstrodb import OnstroDb

schema = {
  "name": {"type": "str"}
}

db = OnstroDb(db_name="test", schema=schema)

db.add([
  {"name": "ad"}
])
db.commit()  # save the changes

print(db)

# output
{'70ba3370': {'name': 'ad'}}

```

> `db.commit()` stores all the current addition and updates in the `.db` file. If not the changes will not be permanent. The commit has no meaning if the DB is an in memory DB

### Adding multiple values.

```python
from onstrodb import OnstroDb

schema = {
  "name": {"type": "str"}
}

db = OnstroDb(db_name="test", schema=schema)

ids = db.add([
  {"name": "ad"},
  {"name": "fred"}
], get_hash_id=True)
db.commit()  # save the changes

print(db)
print(ids)

# output
{'70ba3370': {'name': 'ad'}, 'd0cfc2e5': {'name': 'fred'}}
['70ba3370', 'd0cfc2e5']
```

> The `get_hash_id` param if set to `True` will return a list of all the hash id of the newly added data in the order in which they are inserted.

---
