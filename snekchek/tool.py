# Stdlib
import contextlib
import io
import json
import os
import subprocess  # noqa: B404
import sys

# External Libraries
import pytest
import requests
import twine.commands.upload

# Snekchek
from snekchek.misc import __version__
from snekchek.structure import Linter


def get_tools():
    return Pytest, Pypi


class Pytest(Linter):
    def run(self, _: list) -> None:
        with contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(io.StringIO()):
            exitcode = pytest.main(["--json=.log.json", "-qqqq", "-c", ".snekrc"])
        self.status_code = exitcode

        with open(".log.json") as file:
            data = json.load(file)

        os.remove(".log.json")

        self.hook([
            test for test in data['report']['tests']
            if test['outcome'] == 'failed'
        ])


class Pypi(Linter):
    def run(self, _: list) -> None:
        try:
            with contextlib.redirect_stdout(io.StringIO()), \
                    contextlib.redirect_stderr(io.StringIO()):
                proc = subprocess.Popen(  # noqa: B603
                    [sys.executable, "setup.py", "sdist", "bdist_wheel"],
                    stdout=subprocess.DEVNULL)
                proc.wait()
                twine.commands.upload.upload(
                    [f"dist/*{__version__}*"], self.conf["TWINE_REPOSITORY"],
                    self.conf.as_bool("sign"), self.conf.get("identity"),
                    self.conf["TWINE_USERNAME"], self.conf["TWINE_PASSWORD"],
                    self.conf.get("comment"),
                    self.conf.get("sign-with"), self.confpath,
                    self.conf.get("skip-existing", True), None, None, None)

        except requests.exceptions.HTTPError as err:
            print(err)

        self.hook([])
