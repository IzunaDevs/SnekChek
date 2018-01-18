"""
This file:

- flake8
- flake8-bugbear (ext)
- flake8-import-order (ext)
- flake8-mypy (ext)
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


def get_linters():
    return (Flake8, Vulture)


class Flake8(Linter):
    patt = re.compile(r"(?P<path>[^:]+):(?P<line>[0-9]+):(?P<col>[0-9]+): "
                      r"(?P<errcode>[A-Z][0-9]+) (?P<msg>.+)$\n", re.M)

    def __init__(self):
        super().__init__()
        self.f = io.StringIO()

    def run(self, files):
        with contextlib.redirect_stdout(self.f):
            try:
                sett = ["--config", self.confpath]
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
                      r"(?P<err>unused (class|attribute|function) '[a-zA-Z0-9]+') \((?P<conf>[0-9]+)% confidence")

    def __init__(self):
        super().__init__()
        self.f = io.StringIO()

    def run(self, files):
        vult = vulture.core.Vulture(self.conf.get("verbose", False))
        vult.scavenge(files, self.conf.get("exclude"))
        with contextlib.redirect_stdout(self.f):
            vult.report(self.conf.get("min-confidence", 60), self.conf.get("sort-by-size", False))
        self.f.seek(0)
        matches = self.patt.finditer(self.f.read())
        self.status_code = 1 if matches else 0
        self.hook(list(sorted([x.groupdict() for x in matches], key=lambda x: x["line"])))