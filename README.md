# Onstro DB

[![Azure DevOps builds](https://img.shields.io/azure-devops/build/adwaithrajesh/8d11fcc8-9bf7-41cf-95af-bd240456c13e/7?label=azure%20pipelines&style=for-the-badge)](https://dev.azure.com/adwaithrajesh/adwaith/_build?definitionId=7)
![GitHub](https://img.shields.io/github/license/Adwaith-Rajesh/onstro-db?style=for-the-badge)

A **simple**, **fast** and **strict** DB designed to store and handle large amounts of data.

![https://adwaith-rajesh.github.io/onstro-db/](./docs/onstro-logo.png "onstro-db")

## 🔻 Installation

```commandline
pip install onstro-db
```

## 📚 tl;dr

A simple code snippet on how to use OnstroDB

```python
from onstrodb import OnstroDb

# define the schema for the DB
db_schema = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int", "required": True},
    "place": {"type": "str", "default": "canada"}
}

# initialize the db
db = OnstroDb(db_name="test-db", schema=db_schema)

db.add([
    {"name": "adwaith", "age": 16},
    {"name": "fred", "age": 17, "place": "texas"}
])
db.commit()

```

## ❓ Why use it ?

We all know that [Pandas](https://pandas.pydata.org/) is fast, but it's also really hard to learn for beginners. That's where OnstroDb comes into action. This DB allows you to perform CRUD operations on data, with the speed promised by Pandas. Without you having to know a single thing about pandas. The DB is also strict.,i.e once the schema and the types of the data are defined it cannot be modified. And it also comes with a CLI.

- ### Click [here](https://adwaith-rajesh.github.io/onstro-db/docs/) to see the docs.

## 🤔 Why name it Onstro DB ?

Coz it's supposed to handle m**onstro**us amount of data.

## 🥰 Contributing.

Read the **CONTRIBUTING.md** for the code design style and linting preferences.

Once you've gone though follow theses steps.

- Fork this repo.
- Create a new branch from master. (Very important)
- Make your required changes with good commit messages.
- Write the test to make sure that your changes work.
- Create a pull request.
- Bug the maintainers until it get merged 😊.

## 🙊 Have any issue or feature request.

Create an issue or join our Discord server [Here](https://discord.gg/JmkZqc3s).

---

<h3 align="center"> <img align="center" src="https://forthebadge.com/images/badges/made-with-python.svg" href="https://python.org" ></h3>
