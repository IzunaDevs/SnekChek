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
-

"""

from snekchek.structure import CheckHandler
'''
from snekchek.lint import get_linters
from snekchek.style import get_stylers
from snekchek.secure import get_security
'''

def main():
    handler = CheckHandler()

    for linter in get_linters():
        handler.run_lint(linter)

    for style in get_stylers():
        handler.run_style(styler)

    for security in get_security():
        handler.run_secure(security)

    handler.exit()


if __name__ == "__main__":
    main()
