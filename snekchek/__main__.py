u"""
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
# __future__ imports
from __future__ import absolute_import

# Stdlib
import argparse

# Snekchek
from snekchek.config_gen import generate
from snekchek.lint import get_linters
from snekchek.structure import CheckHandler
from snekchek.style import get_stylers


def run_main(args, do_exit=True):
    u"""Runs the checks and exits.

    To extend this tool, use this function and set do_exit to False
    to get returned the status code.
    """
    if args.init:
        generate()
        return None  # exit after generate instead of starting to lint

    handler = CheckHandler(file=args.config_file,
                           out_json=args.json,
                           files=args.files)

    for style in get_stylers():
        handler.run_linter(style())

    for linter in get_linters():
        handler.run_linter(linter())

    # Somehow one of the linters clears globals in py2?
    from snekchek.secure import get_security
    from snekchek.tool import get_tools

    for security in get_security():
        handler.run_linter(security())

    for tool in get_tools():
        tool = tool()

        # Only run pypi if everything else passed
        if tool.name == u"pypi" and handler.status_code != 0:
            continue

        handler.run_linter(tool)

    if do_exit:
        handler.exit()
    return handler.status_code


def main():
    u"""Main entry point for console commands."""
    parser = argparse.ArgumentParser()
    parser.add_argument(u"--json",
                        help=u"output in JSON format",
                        action=u"store_true",
                        default=False)
    parser.add_argument(u"--config-file",
                        help=u"Select config file to use",
                        default=u".snekrc")
    parser.add_argument(u"files",
                        metavar=u"file",
                        nargs=u"*",
                        default=[],
                        help=u"Files to run checks against")
    parser.add_argument(u"--init",
                        help=u"generate snekrc",
                        action=u"store_true",
                        default=False)

    args = parser.parse_args()

    run_main(args)


if __name__ == u"__main__":
    main()
