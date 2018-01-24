# Stdlib
import contextlib
import io
import subprocess  # noqa: B404
import sys

# External Libraries
import requests
import twine.commands.upload

# Snekchek
from snekchek.misc import __version__
from snekchek.structure import Linter


def get_tools():
    return [Pypi]


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
