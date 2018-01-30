"""
This file contains Style checkers.

Stylers included:
- isort
- yapf
"""

# Stdlib
import contextlib
import io

# External Libraries
from snekchek.structure import Linter


def get_stylers() -> list:
    return ISort, Yapf


class ISort(Linter):
    requires_install = ["isort"]

    def run(self, files: list) -> None:
        import isort

        self.conf['line_length'] = self.conf.as_int('line_length')
        self.conf['sections'] = self.conf.as_list('sections')

        res = []

        for filename in files:
            with contextlib.redirect_stdout(io.StringIO()):  # mute stdout
                sort = isort.SortImports(filename, **self.conf)

            if sort.skipped:
                continue

            self.status_code = self.status_code or (1
                                                    if sort.incorrectly_sorted
                                                    else 0)

            if self.conf.as_bool('inplace'):
                with open(filename, "w") as file:
                    file.write(sort.output)

            else:
                with open(filename) as file:
                    out = io.StringIO()
                    with contextlib.redirect_stdout(out):
                        sort._show_diff(file.read())  # pylint: disable=protected-access
                    out.seek(0)
                    diff = out.read()

                if diff.strip():
                    res.append(diff.strip())

        self.hook(res)


class Yapf(Linter):
    requires_install = ["yapf"]

    def run(self, files: list) -> None:
        import yapf.yapflib.yapf_api

        res = []

        for file in files:
            code, _, changed = yapf.yapflib.yapf_api.FormatFile(
                file, style_config=self.confpath)

            self.status_code = self.status_code or (1 if changed else 0)

            if changed:

                if self.conf.as_bool('inplace'):
                    with open(file, "w") as new_file:
                        new_file.write(code)

                else:
                    res.append(code.strip())

        self.hook(res)
