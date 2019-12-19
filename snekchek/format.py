"""Formatting functions for each linter"""

# __future__ imports
from __future__ import print_function, unicode_literals

# Stdlib
import typing


def flake8_format(data):
    # type: (typing.List[typing.Dict[str, typing.Any]]) -> None
    for row in data:
        print("{path}:{line}:{col}: {errcode} {msg}".format(**row))


def vulture_format(data):
    # type: (typing.List[typing.Dict[str, typing.Any]]) -> None
    for row in data:
        print("{path}:{line}: {err} ({conf}% confidence)".format(**row))


def pylint_format(data):
    # type: (typing.List[typing.Dict[str, typing.Any]]) -> None
    last_path = ''
    for row in data:
        if row["path"] != last_path:
            print("File: {0}".format(row["path"]))
            last_path = row["path"]

        print("{type_}:{line:>3}, {column:>2}: {message} ({symbol})".format(
            type_=row["type"][0].upper(), **row))


def pyroma_format(data):
    # type: (typing.Dict[str, typing.Dict[str, typing.List[str]]]) -> None
    for row in list(data["modules"].values())[0]:
        print(row)


def isort_format(data):
    # type: (typing.List[str]) -> None
    for diff in data:
        print(diff)


def yapf_format(data):
    # type: (typing.List[str]) -> None
    for row in data:
        print(row)


def pypi_format(data):
    # type: (typing.List[str]) -> None
    for row in data:
        print(row)


def safety_format(data):
    # type: (typing.List[typing.Tuple[str]]) -> None
    for row in data:
        print("[{row[4]}] ({row[0]}{row[1]}) {row[3]}".format(row=row))


def dodgy_format(data):
    # type: (typing.List[typing.Tuple[str]]) -> None
    for row in data:
        print("{row[1]}:{row[0]}: {row[2]}".format(row=row))


def pytest_format(data):
    # type: (typing.List[typing.Dict[str, typing.Any]]) -> None
    for test in data:
        print(test["name"])
        print(test["call"]["longrepr"])


def unittest_format(data):
    # type: (typing.List[typing.Tuple[typing.Any, str]]) -> None
    for test in data:
        print("Test '{0}'".format(test[0]._testMethodName))  # pylint: disable=protected-access
        print(test[1])
