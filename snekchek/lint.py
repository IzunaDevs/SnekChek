u"""
This file contains linters.

Linters included:

- flake8
- flake8-bugbear (ext)
- flake8-import-order (ext)
- flake8-mypy (ext)
- flake8-docstrings (ext)
- flake8-todo (ext)
- flake8-requirements (ext)
- flake8-string-format (ext)
- flake8-tidy-import (ext)
- flake8-bandit (ext, bandit)
- pylint
- vulture
- pyroma
"""

# __future__ imports
from __future__ import print_function, with_statement

# Stdlib
import io
import json
import re
import sys

# Snekchek
from snekchek.structure import Linter
from snekchek.utils import redirect_stderr, redirect_stdout


def get_linters():
    return Vulture, Pylint, Pyroma, Flake8


class Flake8(Linter):
    requires_install = [u"flake8"]

    patt = re.compile(
        u"(?P<path>[^:]+):(?P<line>[0-9]+):(?P<col>[0-9]+): "
        u"(?P<errcode>[A-Z][0-9]+) (?P<msg>.+)$\\n", re.M)

    def run(self, files):
        import flake8.main.cli

        if sys.version_info >= (3, 0, 0):
            t = io.StringIO
        else:
            t = io.BytesIO
        file = t()
        with redirect_stdout(file) and redirect_stderr(t()):
            try:
                sett = [u"--config=" + self.confpath]
                sett.extend(files)
                flake8.main.cli.main(sett)
            except SystemExit:
                pass
        file.seek(0)
        matches = list(self.patt.finditer(file.read()))
        self.status_code = 1 if matches else 0
        self.hook(
            list(
                sorted([x.groupdict() for x in matches],
                       key=lambda x: x[u"line"])))


class Vulture(Linter):
    requires_install = [u"vulture"]
    base_pyversion = (3, 0, 0)

    patt = re.compile(
        u"^(?P<path>[^:]+):(?P<line>[0-9]+): "
        u"(?P<err>unused (class|attribute|function) '[a-zA-Z0-9]+') "
        u"\\((?P<conf>[0-9]+)% confidence\\)$")

    def run(self, files):
        import vulture.core

        vult = vulture.core.Vulture(self.conf.as_bool(u"verbose"))
        vult.scavenge(files,
                      [x.strip() for x in self.conf.as_list(u"exclude")])
        if sys.version_info >= (3, 0, 0):
            file = io.StringIO()
        else:
            file = io.BytesIO()
        with redirect_stdout(file):
            vult.report(self.conf.as_int(u"min-confidence"),
                        self.conf.as_bool(u"sort-by-size"))
        file.seek(0)
        matches = list(self.patt.finditer(file.read()))
        self.status_code = 1 if matches else 0
        self.hook(
            list(
                sorted([x.groupdict() for x in matches],
                       key=lambda x: x[u"line"])))


class Pylint(Linter):
    requires_install = [u"pylint"]

    def run(self, files):
        import pylint.lint

        args = [u"-f", u"json"] + files
        if sys.version_info >= (3, 0, 0):
            file = io.StringIO()
        else:
            file = io.BytesIO()
        with redirect_stdout(file):
            if sys.version_info >= (3, 0, 0):
                pylint.lint.Run(args, do_exit=False)
            else:
                pylint.lint.Run(args, exit=False)
        file.seek(0)

        text = file.read()
        data = json.loads(text) if text.strip() else []

        self.status_code = bool(data)

        self.hook(data)


class Pyroma(Linter):
    requires_install = [u"pyroma"]

    def run(self, _):

        if sys.version_info >= (3, 0, 0):
            t = io.StringIO
        else:
            t = io.BytesIO

        file = t()
        with redirect_stdout(file), redirect_stderr(t()):
            # Import pyroma here because it uses logging and sys.stdout
            import pyroma  # noqa pylint: disable=all
            pyroma.run(u"directory", u".")
        file.seek(0)

        text = file.read()

        lines = text.split(u"\n")

        lines.pop(0)
        if sys.version_info >= (3, 0, 0):
            lines.pop(0)

        data = {u"modules": {}}

        module = lines.pop(0)[6:].strip()
        data[u"modules"][module] = []
        lines.pop(0)
        if len(lines) >= 6:
            line = lines.pop(0)
            while line != u"-" * 30:
                data[u"modules"][module].append(line)
                line = lines.pop(0)

        rating = lines.pop(0)
        data[u"rating"] = int(rating[14:-3])
        data[u"rating_word"] = lines.pop(0)

        self.status_code = 0 if data[u"rating"] == 10 else 1

        if data[u"rating"] == 10:
            data = []

        self.hook(data)
