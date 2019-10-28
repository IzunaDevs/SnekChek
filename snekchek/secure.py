u"""
Checkers for security issues in the project.

Checkers included:
- Safety
- Dodgy
"""
# __future__ imports
from __future__ import with_statement

# Stdlib
import io
import json
import os
import sys

# Snekchek
from snekchek.structure import Linter
from snekchek.utils import redirect_stdout


def get_security():
    return Safety, Dodgy


class Safety(Linter):
    requires_install = [u"safety"]

    def run(self, _):
        import safety.cli

        if u"requirements.txt" not in os.listdir(u"."):
            self.hook([])
            return

        if sys.version_info >= (3, 0, 0):
            outfile = io.StringIO()
        else:
            outfile = io.BytesIO()

        try:
            with redirect_stdout(outfile):
                safety.cli.check.callback(self.conf.get(u"pyup_key", ''),
                                          self.conf.get(u"db_path", ''), True,
                                          False, False, False, False,
                                          u"requirements.txt",
                                          self.conf.as_list(u"ignore"), "",
                                          "http", None, 80)
        except SystemExit:
            # Raised by safety
            pass

        outfile.seek(0)
        json_data = json.load(outfile)

        self.status_code = 1 if json_data else 0

        self.hook(json_data)


class Dodgy(Linter):
    requires_install = [u"dodgy"]

    def run(self, _):
        import dodgy.run

        data = dodgy.run.run_checks(u".", self.conf.as_list(u"ignore_paths"))

        self.status_code = 1 if data else 0

        self.hook(data)
