<h1 align="center"> Onstro DB </h1>

Things to know while designing a **schema**. The python type hint for a schema is `dict[str, dict[str, object]]`

The first key represent the column and the mapping to represent the property or in this case the `type` of the data to be accepted in that column.

```python

schema = {
    "name": {"type": "int", "required": True},
    "age:" {"type": "int", "required": True},
    "place": {"type": "str", "default": "canada"},
    "salary": {"type": "float"}
}
```

The type of a variable must be in quotes. And these are all the allowed type. **int**, **str**, **float**, **bool**

- Here, `name`, `age', `place`, `salary`, are the columns in the DB.
- If a field is required and if not provided during addition will cause an error.
- If a fields has default value and if not provided during addition then the values provided as default will be used.
- If a field has a default value. Then the value provided as default must of the same type as the type of the field.
