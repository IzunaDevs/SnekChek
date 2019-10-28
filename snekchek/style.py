u"""
This file contains Style checkers.

Stylers included:
- isort
- yapf
"""
# __future__ imports
from __future__ import with_statement

# Stdlib
import io

# Snekchek
from snekchek.structure import Linter
from snekchek.utils import redirect_stdout


def get_stylers():
    return ISort, Yapf


class ISort(Linter):
    requires_install = [u"isort"]

    def run(self, files):
        import isort

        self.conf[u"line_length"] = self.conf.as_int(u"line_length")
        self.conf[u"sections"] = self.conf.as_list(u"sections")
        self.conf[u"multi_line_output"] = self.conf.as_int(
            u"multi_line_output")

        res = []

        for filename in files:
            with redirect_stdout(io.StringIO()):  # mute stdout
                sort = isort.SortImports(filename, **self.conf)

            if sort.skipped:
                continue

            self.status_code = self.status_code or (
                1 if sort.incorrectly_sorted else 0)

            if self.conf.as_bool(u"inplace"):
                with open(filename, u"w") as file:
                    file.write(sort.output)

            else:
                with open(filename) as file:
                    out = io.StringIO()
                    with redirect_stdout(out):
                        sort._show_diff(file.read())  # pylint: disable=protected-access
                    out.seek(0)
                    diff = out.read()

                if diff.strip():
                    res.append(diff.strip())

        self.hook(res)


class Yapf(Linter):
    requires_install = [u"yapf"]
    base_pyversion = (3, 4, 0)

    def run(self, files):
        import yapf.yapflib.yapf_api

        res = []

        for file in files:
            code, _, changed = yapf.yapflib.yapf_api.FormatFile(
                file, style_config=self.confpath)

            self.status_code = self.status_code or (1 if changed else 0)

            if changed:

                if self.conf.as_bool(u"inplace"):
                    with open(file, u"w") as new_file:
                        new_file.write(code)

                else:
                    res.append(code.strip())

        self.hook(res)
