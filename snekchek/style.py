"""
This file contains Style checkers.

Stylers included:
- isort
- yapf
- black
note that black is not compatible with pylint
"""

# __future__ imports
from __future__ import with_statement, unicode_literals

# Stdlib
import io
import sys
import typing

# Snekchek
from snekchek.structure import Linter
from snekchek.utils import redirect_stderr, redirect_stdout


def get_stylers():  # type: () -> typing.Tuple[typing.Type[Linter], ...]
    return ISort, Yapf, Black


class ISort(Linter):
    requires_install = ["isort"]

    def run(self, files):  # type: (typing.List[str]) -> None
        import isort

        self.conf["line_length"] = self.conf.as_int("line_length")
        self.conf["sections"] = self.conf.as_list("sections")
        self.conf["multi_line_output"] = self.conf.as_int("multi_line_output")

        res = []

        for filename in files:
            with redirect_stdout(io.StringIO()):  # mute stdout
                sort = isort.SortImports(filename, **self.conf)

            if sort.skipped:
                continue

            self.status_code = self.status_code or (
                1 if sort.incorrectly_sorted else 0)

            if self.conf.as_bool("inplace"):
                with io.open(filename, "w", encoding="utf-8") as file:
                    file.write(sort.output)

            else:
                with io.open(filename, encoding="utf-8") as file:
                    out = io.StringIO()
                    with redirect_stdout(out):
                        sort._show_diff(file.read())  # pylint: disable=protected-access
                    out.seek(0)
                    diff = out.read()

                if diff.strip():
                    res.append(diff.strip())

        self.hook(res)


class Yapf(Linter):
    requires_install = ["yapf"]
    base_pyversion = (3, 4, 0)

    def run(self, files):  # type: (typing.List[str]) -> None
        import yapf.yapflib.yapf_api

        res = []

        for file in files:
            code, _, changed = yapf.yapflib.yapf_api.FormatFile(
                file, style_config=self.confpath)

            self.status_code = self.status_code or (1 if changed else 0)

            if changed:

                if self.conf.as_bool("inplace"):
                    with io.open(file, "w", encoding="utf-8") as new_file:
                        new_file.write(code)

                else:
                    res.append(code.strip())

        self.hook(res)


class Black(Linter):
    requires_install = ["black"]
    base_pyversion = (3, 6, 0)  # From black setup.py

    def run(self, files):  # type: (typing.List[str]) -> None
        from black import main, TargetVersion

        conf = self.conf
        file = io.StringIO()
        with redirect_stderr(file):
            try:
                main.callback.__closure__[0].cell_contents(
                    sys,
                    None,
                    conf.as_int("line_length"),
                    list(
                        map(
                            lambda x: getattr(TargetVersion, x),
                            conf.as_list("versions"),
                        )),
                    False,
                    False,
                    False,
                    False,
                    False,
                    True,
                    conf.as_bool("quiet"),
                    False,
                    "",
                    conf["exclude"],
                    tuple(files),
                    self.confpath,
                )
            except SystemExit:
                pass
        file.seek(0)
        self.status_code = "reformatted" in file.read()
        self.hook([])
