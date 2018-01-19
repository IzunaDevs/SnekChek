"""
This file:

- flake8
- flake8-bugbear (ext)
- flake8-import-order (ext)
- flake8-isort (ext)
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

import contextlib
import io
import re

from snekchek.structure import Linter

import flake8.main.cli
import vulture.core
import pylint.lint


def get_linters():
    return Flake8, Vulture, Pylint


class Flake8(Linter):
    patt = re.compile(r"(?P<path>[^:]+):(?P<line>[0-9]+):(?P<col>[0-9]+): "
                      r"(?P<errcode>[A-Z][0-9]+) (?P<msg>.+)$\n", re.M)

    def __init__(self):
        super().__init__()
        self.f = io.StringIO()

    def run(self, files):
        with contextlib.redirect_stdout(self.f):
            try:
                sett = [f"--config={self.confpath}", f"--mypy-config={self.confpath}", "--no-isort-config"]
                sett.extend(files)
                flake8.main.cli.main(sett)
            except SystemExit:
                print("aaa")
        self.f.seek(0)
        matches = self.patt.finditer(self.f.read())
        self.status_code = 1 if matches else 0
        self.hook(list(sorted([x.groupdict() for x in matches], key=lambda x: x["line"])))


class Vulture(Linter):
    patt = re.compile(r"(?P<path>[^:]+):(?P<line>[0-9]+): "
                      r"(?P<err>unused (class|attribute|function) '[a-zA-Z0-9]+') "
                      r"\((?P<conf>[0-9]+)% confidence")

    def __init__(self):
        super().__init__()
        self.f = io.StringIO()

    def run(self, files):
        vult = vulture.core.Vulture(False if self.conf.get("verbose", 'false') == 'false' else True)
        vult.scavenge(files, [x.strip() for x in self.conf.get("exclude", '').split(",")])
        with contextlib.redirect_stdout(self.f):
            vult.report(int(self.conf.get("min-confidence", 60)),
                        False if self.conf.get("sort-by-size", 'false') == 'false' else True)
        self.f.seek(0)
        matches = self.patt.finditer(self.f.read())
        self.status_code = 1 if matches else 0
        self.hook(list(sorted([x.groupdict() for x in matches], key=lambda x: x["line"])))


class Pylint(Linter):
    def __init__(self):
        super().__init__()
        self.f = io.StringIO()

    def run(self, files):
        args = ["-f", "json"] + files
        with contextlib.redirect_stdout(self.f):
            pylint.lint.Run(args, exit=False)
        self.f.seek(0)

        text = self.f.read()
        self.status_code = 1 if text.strip() else 0

        data = json.loads(text)
        print(data)
        self.hook(data)
