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

import flake8.api.legacy


def get_linters():
    return (Flake8,)


class Flake8(Linter):
    type_ = "extension"
    return_type = "json"

    patt = re.compile(r"(?P<path>[^:]+):(?P<line>[0-9]+):(?P<col>[0-9]+): "
                      r"(?P<errcode>[A-Z][0-9]+) (?P<msg>.+)$\n", re.M)

    def __init__(self):
        super().__init__()

        self.out = ""
        self.style = flake8.api.legacy.get_style_guide()
        self.f = io.StringIO()

    def run(self, files):
        with contextlib.redirect_stdout(self.f):
            status = self.style.check_files(files)
        self.f.seek(0)
        self.status_code = 1 if status.total_errors else 0
        matches = self.patt.finditer(self.f.read())
        self.hook(list(sorted([x.groupdict() for x in matches], key=lambda x: x["line"])))
