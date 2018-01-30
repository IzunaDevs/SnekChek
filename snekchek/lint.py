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
from snekchek.structure import Linter


def get_linters() -> list:
    return Vulture, Pylint, Pyroma, Flake8


class Flake8(Linter):
    requires_install = ["flake8"]

    patt = re.compile(r"(?P<path>[^:]+):(?P<line>[0-9]+):(?P<col>[0-9]+): "
                      r"(?P<errcode>[A-Z][0-9]+) (?P<msg>.+)$\n", re.M)

    def run(self, files: list) -> None:
        import flake8.main.cli

        file = io.StringIO()
        with contextlib.redirect_stdout(file):
            try:
                sett = [f"--config={self.confpath}"]
                sett.extend(files)
                flake8.main.cli.main(sett)
            except SystemExit:
                print("aaa")
        file.seek(0)
        matches = list(self.patt.finditer(file.read()))
        self.status_code = 1 if matches else 0
        self.hook(
            list(
                sorted(
                    [x.groupdict() for x in matches],
                    key=lambda x: x["line"])))


class Vulture(Linter):
    requires_install = ["vulture"]

    patt = re.compile(
        r"(?P<path>[^:]+):(?P<line>[0-9]+): "
        r"(?P<err>unused (class|attribute|function) '[a-zA-Z0-9]+') "
        r"\((?P<conf>[0-9]+)% confidence")

    def run(self, files: list) -> None:
        import vulture.core

        vult = vulture.core.Vulture(self.conf.as_bool('verbose'))
        vult.scavenge(files, [x.strip() for x in self.conf.as_list("exclude")])
        file = io.StringIO()
        with contextlib.redirect_stdout(file):
            vult.report(
                self.conf.as_int("min-confidence"),
                self.conf.as_bool("sort-by-size"))
        file.seek(0)
        matches = list(self.patt.finditer(file.read()))
        self.status_code = 1 if matches else 0
        self.hook(
            list(
                sorted(
                    [x.groupdict() for x in matches],
                    key=lambda x: x["line"])))


class Pylint(Linter):
    requires_install = ["pylint"]

    def run(self, files: list) -> None:
        import pylint.lint

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
    requires_install = ["pyroma"]

    def run(self, _: list) -> None:
        file = io.StringIO()
        with contextlib.redirect_stdout(file), contextlib.redirect_stderr(
                io.StringIO()):
            # Import pyroma here because it uses logging and sys.stdout
            import pyroma  # noqa pylint: disable=all
            pyroma.run('directory', '.')
        file.seek(0)

        text = file.read()

        lines = text.split("\n")

        lines.pop(0)
        lines.pop(0)

        data = {'modules': {}}

        module = lines.pop(0)[6:].strip()
        data['modules'][module] = []
        lines.pop(0)
        if len(lines) >= 6:
            line = lines.pop(0)
            while line != "-" * 30:
                data['modules'][module].append(line)
                line = lines.pop(0)

        rating = lines.pop(0)
        data['rating'] = int(rating[14:-3])
        data['rating_word'] = lines.pop(0)

        self.status_code = 0 if data['rating'] == 10 else 1

        if data['rating'] == 10:
            data = []

        self.hook(data)
