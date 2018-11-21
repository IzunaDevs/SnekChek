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

        with redirect_stdout(sys.stderr):
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
                    twine.Settings(
                        sign=self.conf.as_bool("sign"),
                        repository_url=self.conf["TWINE_REPOSITORY"],
                        username=self.conf["TWINE_USERNAME"],
                        identity=self.conf.get("identity"),
                        password=self.conf["TWINE_PASSWORD"],
                        comment=self.conf.get("comment"),
                        sign_with=self.conf.get("sign-with"),
                        config_file=self.confpath,
                        skip_existing= self.conf.get("skip-existing", True)
                    )
                    ["dist/*{0}*".format(__version__)]  # TODO: Fix this to use generic version from any project
                )

        except requests.exceptions.HTTPError as err:
            print(err)

        self.hook([])
