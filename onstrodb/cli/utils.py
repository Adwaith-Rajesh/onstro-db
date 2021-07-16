import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any
from typing import Dict

from onstrodb import __version__
from onstrodb import OnstroDb
from onstrodb.errors import SchemaError


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def cmd_parser(args: Dict[str, Any]) -> int:

    # the main cmd
    if args["version"]:
        print(__version__, file=sys.stdout)
        return 0

    # the sub commands

    if args["sub_command"]:
        sub_command: str = args["sub_command"]

        if sub_command == "create":
            try:
                schema = load_json(args["schema"])

                try:
                    o = OnstroDb(db_name=args["name"],
                                 schema=schema, db_path=args["d"])
                    o.commit()
                    return 0

                except SchemaError:
                    print("Invalid Schema", file=sys.stderr)
                    return 1

            except FileNotFoundError:
                print(
                    f"The file {args['schema']} does not exists", file=sys.stderr)
                return 1

        if sub_command == "delete":
            path = os.path.join(args["d"], args["name"])
            if Path(path).is_dir():
                shutil.rmtree(path)
                return 0

            else:
                print("The DB does not exists", file=sys.stderr)
                return 1

        if sub_command == "purge":
            db_file_path = os.path.join(
                args["d"], args["name"], f"{args['name']}.db")
            schema_file = os.path.join(args["d"], args["name"], "db.schema")

            if Path(db_file_path).is_file():
                if Path(schema_file).is_file():
                    o = OnstroDb(db_name=args["name"],
                                 db_path=args["d"])
                    o.purge()
                    o.commit()

                else:
                    print(
                        f"Schema does no exists for the DB {args['name']}", file=sys.stderr)
                    return 1

            else:
                print(
                    f"The DB file does not exists ({args['name']}.db)", file=sys.stderr)
                return 1

    return 0
