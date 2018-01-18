"""
Linter/Styler/Checker combined for:

- flake8
- flake8-bugbear (ext)
- flake8-import-order (ext)
- flake8-mypy (ext)
- pylint
- yapf
- isort
- pyroma
- safety
- bandit
- dodgy
- pydocstyle
- vulture
- pytest
- Upload to pypi


Implemented:
- flake8
- flake8-bugbear (ext)
- flake8-import-order (ext)
- flake8-mypy (ext)

"""

from snekchek.structure import CheckHandler

from snekchek.lint import get_linters
from snekchek.style import get_stylers
from snekchek.secure import get_security


def main():
    handler = CheckHandler()

    for linter in get_linters():
        handler.run_linter(linter())

    for style in get_stylers():
        handler.run_linter(style())

    for security in get_security():
        handler.run_linter(security())

    handler.exit()


if __name__ == "__main__":
    main()
