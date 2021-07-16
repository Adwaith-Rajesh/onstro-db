import argparse

from .common import add_common_cmds
from .utils import cmd_parser


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")

    sub_parser = parser.add_subparsers(dest="sub_command")

    add_common_cmds(sub_parser)

    args = parser.parse_args()
    rv = cmd_parser(vars(args))

    return rv
