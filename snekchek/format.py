u"""Formatting functions for each linter"""
# __future__ imports
from __future__ import print_function

# Stdlib
import typing


def flake8_format(
        data, ):  # type: (typing.List[typing.Dict[str, typing.Any]]) -> None
    for row in data:
        print(u"{path}:{line}:{col}: {errcode} {msg}".format(**row))


def vulture_format(
        data, ):  # type: (typing.List[typing.Dict[str, typing.Any]]) -> None
    for row in data:
        print(u"{path}:{line}: {err} ({conf}% confidence)".format(**row))


def pylint_format(
        data, ):  # type: (typing.List[typing.Dict[str, typing.Any]]) -> None
    last_path = ''
    for row in data:
        if row[u"path"] != last_path:
            print(u"File: {0}".format(row[u"path"]))
            last_path = row[u"path"]

        print(u"{type_}:{line:>3}, {column:>2}: {message} ({symbol})".format(
            type_=row[u"type"][0].upper(), **row))


def pyroma_format(
        data,
):  # type: (typing.Dict[str, typing.Dict[str, typing.List[str]]]) -> None
    for row in list(data[u"modules"].values())[0]:
        print(row)


def isort_format(data):  # type: (typing.List[str]) -> None
    for diff in data:
        print(diff)


def yapf_format(data):  # type: (typing.List[str]) -> None
    for row in data:
        print(row)


def pypi_format(data):  # type: (typing.List[str]) -> None
    for row in data:
        print(row)


def safety_format(data):  # type: (typing.List[typing.Tuple[str]]) -> None
    for row in data:
        print(u"[{row[4]}] ({row[0]}{row[1]}) {row[3]}".format(row=row))


def dodgy_format(data):  # type: (typing.List[typing.Tuple[str]]) -> None
    for row in data:
        print(u"{row[1]}:{row[0]}: {row[2]}".format(row=row))


def pytest_format(
        data, ):  # type: (typing.List[typing.Dict[str, typing.Any]]) -> None
    for test in data:
        print(test[u"name"])
        print(test[u"call"][u"longrepr"])


def unittest_format(
        data, ):  # type: (typing.List[typing.Tuple[typing.Any, str]]) -> None
    for test in data:
        print("Test '{0}'".format(test[0]._testMethodName))  # pylint: disable=protected-access
        print(test[1])
