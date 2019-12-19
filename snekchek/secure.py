"""
Checkers for security issues in the project.

Checkers included:
- Safety
- Dodgy
(bandit is supported in flake8-bandit)
"""

# __future__ imports
from __future__ import with_statement, unicode_literals

# Stdlib
import io
import json
import os
import sys
import typing

# Snekchek
from snekchek.structure import Linter
from snekchek.utils import redirect_stdout


def get_security():  # type: () -> typing.Tuple[typing.Type[Linter], ...]
    return Safety, Dodgy


class Safety(Linter):
    requires_install = ["safety"]

    def run(self, _):  # type: (typing.List[str]) -> None
        import safety.cli

        if "requirements.txt" not in os.listdir("."):
            self.hook([])
            return

        if sys.version_info >= (3, 0, 0):
            outfile = io.StringIO()
        else:
            outfile = io.BytesIO()

        try:
            with redirect_stdout(outfile):
                safety.cli.check.callback(
                    self.conf.get("pyup_key", ''),
                    self.conf.get("db_path", ''),
                    True,
                    False,
                    False,
                    False,
                    False,
                    "requirements.txt",
                    self.conf.as_list("ignore"),
                    "",
                    "http",
                    None,
                    80,
                )
        except SystemExit:
            # Raised by safety
            pass

        outfile.seek(0)
        json_data = json.load(outfile)

        self.status_code = 1 if json_data else 0

        self.hook(json_data)


class Dodgy(Linter):
    requires_install = ["dodgy"]

    def run(self, _):  # type: (typing.List[str]) -> None
        import dodgy.run

        data = dodgy.run.run_checks(".", self.conf.as_list("ignore_paths"))

        self.status_code = 1 if data else 0

        self.hook(data)
