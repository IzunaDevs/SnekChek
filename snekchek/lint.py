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

# Stdlib
import contextlib
import io
import json
import re

# External Libraries
import flake8.main.cli
import pylint.lint
import vulture.core

# Snekchek
from snekchek.structure import Linter


def get_linters():
    return Vulture, Pylint, Pyroma, Flake8


class Flake8(Linter):
    patt = re.compile(r"(?P<path>[^:]+):(?P<line>[0-9]+):(?P<col>[0-9]+): "
                      r"(?P<errcode>[A-Z][0-9]+) (?P<msg>.+)$\n", re.M)

    def run(self, files):
        file = io.StringIO()
        with contextlib.redirect_stdout(file):
            try:
                sett = [f"--config={self.confpath}",
                        f"--mypy-config={self.confpath}"]
                sett.extend(files)
                flake8.main.cli.main(sett)
            except SystemExit:
                print("aaa")
        file.seek(0)
        matches = self.patt.finditer(file.read())
        self.status_code = 1 if matches else 0
        self.hook(list(sorted([x.groupdict() for x in matches], key=lambda x: x["line"])))


class Vulture(Linter):
    patt = re.compile(r"(?P<path>[^:]+):(?P<line>[0-9]+): "
                      r"(?P<err>unused (class|attribute|function) '[a-zA-Z0-9]+') "
                      r"\((?P<conf>[0-9]+)% confidence")

    def run(self, files):
        vult = vulture.core.Vulture(
            False if self.conf.get("verbose", 'false') == 'false' else True)
        vult.scavenge(files, [x.strip() for x in self.conf.get("exclude", '').split(",")])
        file = io.StringIO()
        with contextlib.redirect_stdout(file):
            vult.report(int(self.conf.get("min-confidence", 60)),
                        False if self.conf.get("sort-by-size", 'false') == 'false' else True)
        file.seek(0)
        matches = self.patt.finditer(file.read())
        self.status_code = 1 if matches else 0
        self.hook(list(sorted([x.groupdict() for x in matches], key=lambda x: x["line"])))


class Pylint(Linter):
    def run(self, files):
        args = ["-f", "json"] + files
        file = io.StringIO()
        with contextlib.redirect_stdout(file):
            pylint.lint.Run(args, exit=False)
        file.seek(0)

        text = file.read()
        self.status_code = 1 if text.strip() else 0

        data = json.loads(text) if text.strip() else []
        self.hook(data)


class Pyroma(Linter):
    def run(self, _):
        file = io.StringIO()
        with contextlib.redirect_stdout(file):
            # Import pyroma here because it uses logging and sys.stdout
            import pyroma  # noqa pylint: disable=all
            pyroma.run('directory', '.')
        file.seek(0)

        text = file.read()

        lines = text.split("\n")

        lines.pop(0)
        lines.pop(0)

        data = {}

        module = lines.pop(0)[6:].strip()
        data[module] = []
        lines.pop(0)
        line = lines.pop(0)
        while line != "-" * 30:
            data[module].append(line)
            line = lines.pop(0)

        data['rating'] = int(lines.pop(0)[14:-3])
        data['rating_word'] = lines.pop(0)

        self.status_code = 0 if data['rating'] == 10 else 1

        self.hook(data)
