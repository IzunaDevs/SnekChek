u"""Formatting functions for each linter"""
# __future__ imports
from __future__ import print_function


def flake8_format(data):
    for row in data:
        print(u"{path}:{line}:{col}: {errcode} {msg}".format(**row))


def vulture_format(data):
    for row in data:
        print(u"{path}:{line}: {err} ({conf}% confidence)".format(**row))


def pylint_format(data):
    last_path = ''
    for row in data:
        if row[u"path"] != last_path:
            print(u"File: {0}".format(row[u"path"]))
            last_path = row[u"path"]

        print(u"{type_}:{line:>3}, {column:>2}: {message} ({symbol})".format(
            type_=row[u"type"][0].upper(), **row))


def pyroma_format(data):
    for row in list(data[u"modules"].values())[0]:
        print(row)


def isort_format(data):
    for diff in data:
        print(diff)


def yapf_format(data):
    for row in data:
        print(row)


def pypi_format(data):
    for row in data:
        print(row)


def safety_format(data):
    for row in data:
        print(u"[{row[4]}] ({row[0]}{row[1]}) {row[3]}".format(row=row))


def dodgy_format(data):
    for row in data:
        print(u"{row[1]}:{row[0]}: {row[2]}".format(row=row))


def pytest_format(data):
    for test in data:
        print(test[u"name"])
        print(test[u"call"][u"longrepr"])
