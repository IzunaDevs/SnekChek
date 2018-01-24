# Stdlib
import contextlib
import io
import json
import os

# External Libraries
import safety.cli

# Snekchek
from snekchek.structure import Linter


def get_security() -> list:
    return [Safety]


class Safety(Linter):
    def run(self, _: list) -> None:
        if "requirements.txt" not in os.listdir():
            self.hook([])
            return

        outfile = io.StringIO()

        try:
            with contextlib.redirect_stdout(outfile):
                safety.cli.check.callback(
                    self.conf.get("pyup_key", ""), self.conf.get(
                        "db_path", ""), True, False, False, False, False,
                    "requirements.txt", self.conf.as_list("ignore"))
        except SystemExit:
            # Raised by safety
            pass

        outfile.seek(0)

        json_data = json.load(outfile)

        self.status_code = 1 if json_data else 0

        self.hook(json_data)
