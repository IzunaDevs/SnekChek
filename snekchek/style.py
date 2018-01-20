"""
This file contains Style checkers.

Stylers included:

- isort
- yapf
- pydocstyle
"""

# Stdlib
import contextlib
import io

# External Libraries
import isort
from snekchek.structure import Linter


def get_stylers():
    return [ISort]


class ISort(Linter):
    def run(self, files):
        sett = dict(**self.conf)
        sett['line_length'] = int(sett['line_length'])
        sett['sections'] = sett['sections'].split(",")

        res = []

        for filename in files:
            with contextlib.redirect_stdout(io.StringIO()):  # mute stdout
                sort = isort.SortImports(filename, **sett)

            if sort.skipped:
                continue

            self.status_code = self.status_code or (1 if sort.incorrectly_sorted else 0)

            if True if sett['inplace'] == 'true' else False:
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
