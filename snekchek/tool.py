u"""
Tools to run over code that don't lint and don't format

Currently included:
- Pytest
- Upload to pypi (twine)
"""
# __future__ imports
from __future__ import print_function, with_statement

# Stdlib
import glob
import io
import json
import os
import subprocess  # noqa: B404
import sys
import typing

# Snekchek
from snekchek.misc import __version__
from snekchek.structure import Linter
from snekchek.utils import redirect_stderr, redirect_stdout


def get_tools():  # type: () -> typing.Tuple[typing.Type[Linter], ...]
    return Pytest, UnitTest, Pypi


class Pytest(Linter):
    requires_install = [u"pytest", u"pytest-json"]

    def run(self, _):  # type: (typing.List[str]) -> None
        import pytest

        if sys.version_info >= (3, 0, 0):
            file = io.StringIO()
        else:
            file = io.BytesIO()

        with redirect_stdout(file):
            with redirect_stderr(file):
                exitcode = pytest.main(
                    [u"--json=.log.json", u"-qqqq", u"-c", self.confpath])
        self.status_code = exitcode

        with open(u".log.json", encoding="utf-8") as file:
            data = json.load(file)

        os.remove(u".log.json")

        self.hook([
            test for test in data[u"report"][u"tests"]
            if test[u"outcome"] == u"failed"
        ])


class UnitTest(Linter):
    def run(self, _):  # type: (typing.List[str]) -> None
        from unittest.main import TestProgram

        errors = []

        if sys.version_info >= (3, 0, 0):
            fileo = io.StringIO()
        else:
            fileo = io.BytesIO()

        with redirect_stderr(fileo):
            paths = glob.glob(self.conf["testpaths"])
            if len(paths) == 1 and os.path.isdir(paths[0]):
                paths = [
                    paths[0] + "/" + path for path in os.listdir(paths[0])
                ]

            for path in paths:
                test_name = path.split(".")[0].replace("/", ".")
                prog = TestProgram(test_name, exit=False)
                errors += prog.result.errors
                errors += prog.result.failures

        fileo.seek(0)
        self.status_code = bool(errors)
        self.hook(errors)


class Pypi(Linter):
    requires_install = [u"twine", u"wheel", u"requests"]

    def run(self, _):  # type: (typing.List[str]) -> None
        import requests
        import twine.commands.upload
        import twine.settings

        try:
            with redirect_stdout(io.StringIO()), \
                    redirect_stderr(io.StringIO()):

                if sys.version_info >= (3, 0, 0):
                    proc = subprocess.Popen(  # noqa: B603
                        [
                            sys.executable,
                            u"setup.py",
                            u"sdist",
                            u"bdist_wheel",
                        ],
                        stdout=subprocess.DEVNULL,
                    )
                else:
                    proc = subprocess.Popen(  # noqa: B603
                        [
                            sys.executable, u"setup.py", u"sdist",
                            u"bdist_wheel"
                        ])
                proc.wait()
                twine.commands.upload.upload(
                    twine.settings.Settings(
                        sign=self.conf.as_bool(u"sign"),
                        repository=self.conf[u"TWINE_REPOSITORY"],
                        username=self.conf[u"TWINE_USERNAME"],
                        identity=self.conf.get(u"identity"),
                        password=self.conf[u"TWINE_PASSWORD"],
                        comment=self.conf.get(u"comment"),
                        sign_with=self.conf.get(u"sign-with"),
                        config_file=self.confpath,
                        skip_existing=self.conf.get(u"skip-existing", True),
                    ),
                    [
                        u"dist/*{0}*".format(
                            self.conf.get(u"version", __version__))
                    ],
                )  # noqa

        except requests.exceptions.HTTPError as err:
            print(err)

        self.hook([])
