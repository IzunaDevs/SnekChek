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

import argparse
from snekchek.structure import CheckHandler

from snekchek.lint import get_linters
from snekchek.style import get_stylers
from snekchek.secure import get_security


def run_main(args):
    handler = CheckHandler(file=args.config_file, out_json=args.json)

    for linter in get_linters():
        handler.run_linter(linter())

    for style in get_stylers():
        handler.run_linter(style())

    for security in get_security():
        handler.run_linter(security())

    handler.exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="output in JSON format", action="set_true", default=False)
    parser.add_argument("--config-file", help="Select config file to use", default=".snekrc")
    args = parser.parse_args()

    run_main(args)


if __name__ == "__main__":
    main()
