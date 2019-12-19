"""
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
from __future__ import print_function, with_statement, unicode_literals

# Stdlib
import io
import json
import os
import re
import sys
import typing

# Snekchek
from snekchek.structure import Linter
from snekchek.utils import redirect_stderr, redirect_stdout


def get_linters():  # type: () -> typing.Tuple[typing.Type[Linter], ...]
    return Vulture, Pylint, Pyroma, Flake8


class Flake8(Linter):
    requires_install = ["flake8"]

    patt = re.compile(
        "(?P<path>[^:]+):(?P<line>[0-9]+):(?P<col>[0-9]+): "
        "(?P<errcode>[A-Z][0-9]+) (?P<msg>.+)$\\n",
        re.M,
    )

    def run(self, files):  # type: (typing.List[str]) -> None
        # Flake8 has some issues with logging for some reason idk
        from logging import StreamHandler
        old_emit, StreamHandler.emit = StreamHandler.emit, lambda *_: None

        import flake8.main.cli
        try:
            sett = [
                u"--config=" + self.confpath, u"--output-file=.flake8_output"
            ]
            sett.extend(files)
            flake8.main.cli.main(sett)
        except SystemExit:
            pass

        # revert flake8 compat
        StreamHandler.emit = old_emit

        with open(".flake8_output") as file:
            matches = list(self.patt.finditer(file.read()))
            self.status_code = 1 if matches else 0
            self.hook(
                list(
                    sorted([x.groupdict() for x in matches],
                           key=lambda x: x["line"])))
        if os.path.exists(".flake8_output"):
            os.remove(".flake8_output")


class Vulture(Linter):
    requires_install = ["vulture"]
    base_pyversion = (3, 0, 0)

    patt = re.compile(
        "^(?P<path>[^:]+):(?P<line>[0-9]+): "
        "(?P<err>unused (class|attribute|function) '[a-zA-Z0-9]+') "
        "\\((?P<conf>[0-9]+)% confidence\\)$")

    def run(self, files):  # type: (typing.List[str]) -> None
        import vulture.core

        vult = vulture.core.Vulture(self.conf.as_bool("verbose"))
        vult.scavenge(files, [x.strip() for x in self.conf.as_list("exclude")])
        if sys.version_info >= (3, 0, 0):
            file = io.StringIO()
        else:
            file = io.BytesIO()
        with redirect_stdout(file):
            vult.report(
                self.conf.as_int("min-confidence"),
                self.conf.as_bool("sort-by-size"),
            )
        file.seek(0)
        matches = list(self.patt.finditer(file.read()))
        self.status_code = 1 if matches else 0
        self.hook(
            list(
                sorted([x.groupdict() for x in matches],
                       key=lambda x: x["line"])))


class Pylint(Linter):
    requires_install = ["pylint"]

    def run(self, files):  # type: (typing.List[str]) -> None
        args = ["-f", "json"] + files
        if sys.version_info >= (3, 0, 0):
            file = io.StringIO()
        else:
            file = io.BytesIO()

        with redirect_stdout(sys.stderr), redirect_stderr(file):
            import pylint.lint

            if sys.version_info < (3, 0, 0):
                from pylint.reporters.json import JSONReporter
                JSONReporter.__init__.__func__.__defaults__ = (file, )
            else:
                from pylint.reporters.json_reporter import JSONReporter
                JSONReporter.__init__.__defaults__ = (file, )

            if sys.version_info >= (3, 0, 0):
                pylint.lint.Run(args, do_exit=False)
            else:
                pylint.lint.Run(args, exit=False)
        file.seek(0)

        text = file.read()

        if text.startswith("Using config file"):
            text = "\n".join(text.split("\n")[1:])

        data = json.loads(text) if text.strip() else []

        self.status_code = bool(data)

        self.hook(data)


class Pyroma(Linter):
    requires_install = ["pyroma"]

    def run(self, _):  # type: (typing.List[str]) -> None

        if sys.version_info >= (3, 0, 0):
            t = io.StringIO
        else:
            t = io.BytesIO

        file = t()
        with redirect_stdout(file), redirect_stderr(file):
            # Import pyroma here because it uses logging and sys.stdout
            import pyroma  # noqa pylint: disable=all

            pyroma.run("directory", ".")
        file.seek(0)

        text = file.read()

        lines = text.split("\n")
        lines.pop(0)
        if sys.version_info >= (3, 0, 0):
            lines.pop(0)

        data = {"modules": {}}

        module = lines.pop(0)[6:].strip()
        data["modules"][module] = []
        lines.pop(0)
        if len(lines) >= 6:
            line = lines.pop(0)
            while line != "-" * 30:
                data["modules"][module].append(line)
                line = lines.pop(0)

        rating = lines.pop(0)
        data["rating"] = int(rating[14:-3])
        data["rating_word"] = lines.pop(0)

        self.status_code = 0 if data["rating"] == 10 else 1

        if data["rating"] == 10:
            data = []

        self.hook(data)
