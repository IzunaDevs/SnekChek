"""
Linter/Styler/Checker combined for linters.

Linters supported:

- flake8
- flake8-bugbear (ext)
- flake8-import-order (ext)
- flake8-docstrings (ext)
- flake8-todo (ext)
- flake8-requirements (ext)
- flake8-string-format (ext)
- flake8-tidy-import (ext)
- flake8-bandit (ext, bandit)
- pylint
- yapf
- isort
- pyroma
- safety
- bandit
- dodgy
- vulture
- pytest
- Upload to pypi
"""

# Stdlib
import argparse

# External Libraries
from snekchek.lint import get_linters
from snekchek.secure import get_security
from snekchek.structure import CheckHandler
from snekchek.style import get_stylers
from snekchek.tool import get_tools


def run_main(args: argparse.Namespace, do_exit=True) -> None:
    """Runs the checks and exits.

    To extend this tool, use this function and set do_exit to False
    to get returned the status code.
    """
    handler = CheckHandler(file=args.config_file, out_json=args.json)

    for style in get_stylers():
        handler.run_linter(style())

    for linter in get_linters():
        handler.run_linter(linter())

    for security in get_security():
        handler.run_linter(security())

    for tool in get_tools():
        tool = tool()

        # Only run pypi if everything else passed
        if tool.name == "pypi" and handler.status_code != 0:
            continue

        handler.run_linter(tool)

    if do_exit:
        handler.exit()
    return handler.status_code


def main() -> None:
    """Main entry point for console commands."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json",
        help="output in JSON format",
        action="store_true",
        default=False)
    parser.add_argument(
        "--config-file", help="Select config file to use", default=".snekrc")
    args = parser.parse_args()

    run_main(args)


if __name__ == "__main__":
    main()
