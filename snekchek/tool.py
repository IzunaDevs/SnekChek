"""
Tools to run over code that don't lint and don't format

Currently included:
- Pytest
- Upload to pypi (twine)
"""

# Stdlib
import io
import json
import os
import subprocess  # noqa: B404
import sys

# External Libraries
from snekchek.misc import __version__
from snekchek.structure import Linter
from snekchek.utils import redirect_stderr, redirect_stdout


def get_tools():
    return Pytest, Pypi


class Pytest(Linter):
    requires_install = ["pytest", "pytest-json"]

    def run(self, _: list) -> None:
        import pytest

        exitcode = pytest.main(
            ["--json=.log.json", "-qqqq", "-c", self.confpath])
        self.status_code = exitcode

        with open(".log.json") as file:
            data = json.load(file)

        os.remove(".log.json")

        self.hook([
            test for test in data['report']['tests']
            if test['outcome'] == 'failed'
        ])


class Pypi(Linter):
    requires_install = ["twine", "wheel", "requests"]

    def run(self, _: list) -> None:
        import requests
        import twine.commands.upload

        try:
            with redirect_stdout(io.StringIO()), \
                    redirect_stderr(io.StringIO()):
                proc = subprocess.Popen(  # noqa: B603
                    [sys.executable, "setup.py", "sdist", "bdist_wheel"],
                    stdout=subprocess.DEVNULL)
                proc.wait()
                twine.commands.upload.upload(
                    ["dist/*{0}*".format(__version__)],
                    self.conf["TWINE_REPOSITORY"], self.conf.as_bool("sign"),
                    self.conf.get("identity"), self.conf["TWINE_USERNAME"],
                    self.conf["TWINE_PASSWORD"], self.conf.get("comment"),
                    self.conf.get("sign-with"), self.confpath,
                    self.conf.get("skip-existing", True), None, None, None)

        except requests.exceptions.HTTPError as err:
            print(err)

        self.hook([])
