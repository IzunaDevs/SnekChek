u""" Common classes and utility functions. """
# __future__ imports
from __future__ import print_function

# Stdlib
import json
import os
import re
import subprocess  # noqa: B404
import sys

# Snekchek
import snekchek.format


def flatten(nested_list):
    u"""Flattens a list, ignore all the lambdas."""
    return list(
        sorted(
            filter(
                lambda y: y is not None,
                list(
                    map(
                        lambda x: (
                            nested_list.extend(x)  # noqa: T484
                            if isinstance(x, list) else x),
                        nested_list)))))


def get_py_files(dir_name):
    u"""Get all .py files."""
    return flatten([
        x for x in
        [[u"{0}/{1}".format(path, f) for f in files if f.endswith(u".py")]
         for path, _, files in os.walk(dir_name)
         if not path.startswith(u"./build")] if x
    ])


class ModuleNotInstalled(Exception):
    pass


class CheckHandler(object):
    def __init__(self, file, out_json, check_dir=u".", files=None):
        # Do this here so setup.py doesn't error
        from snekchek.baseconfig import config
        import configobj
        if not os.path.isfile(file):
            print(u"config file not found: {0}".format(file))
            if file != u".snekrc":
                print(u"trying snekrc...")
                if not os.path.isfile(u".snekrc"):
                    print(u"no config found falling back to default")
                else:
                    file = u".snekrc"
            else:
                print(u"no config found falling back to default")
        self.parser = config
        self.parser.merge(configobj.ConfigObj(file))

        self.fn = file  # pylint: disable=invalid-name
        self.status_code = 0
        self.logs = {}
        self.current = ''
        self.json = out_json

        self.indent = 4 if u"--debug" in sys.argv else None

        self.files = files or get_py_files(check_dir)

        patt = re.compile(u"^(?P<package>\\S+?)\\s*(?P<version>\\S+)\\s*$",
                          re.M)

        args = [sys.executable, u"-m", u"pip", u"list"]

        proc = subprocess.Popen(  # noqa: B603
            args, stdout=subprocess.PIPE)

        proc.wait()

        matches = list(patt.finditer(proc.stdout.read().decode()))[
            2:]  # [2:] to remove title and the dashes

        self.installed = [p.group(u"package") for p in matches]

    def exit(self):
        u"""Raise SystemExit with correct status code and output logs."""
        total = sum(len(logs) for logs in self.logs.values())
        if self.json:
            self.logs[u"total"] = total
            print(json.dumps(self.logs, indent=self.indent))

        else:
            for name, log in self.logs.items():
                if not log or self.parser[name].as_bool(u"quiet"):
                    continue

                print(u"[[{0}]]".format(name))
                getattr(snekchek.format, name + u"_format")(log)
                print(u"\n")

            print(u"-" * 30)
            print(u"Total:", total)

        sys.exit(self.status_code)

    def run_linter(self, linter):
        u"""Run a checker class"""
        self.current = linter.name

        if (linter.name not in self.parser[u"all"].as_list(u"linters")
                or linter.base_pyversion > sys.version_info):  # noqa: W503
            return

        if any(x not in self.installed for x in linter.requires_install):
            raise ModuleNotInstalled(linter.requires_install)

        linter.add_output_hook(self.out_func)
        linter.set_config(self.fn, self.parser[linter.name])
        linter.run(self.files)
        self.status_code = self.status_code or linter.status_code

    def out_func(self, data):
        self.logs[self.current] = data


class Linter(object):
    u"""Common shared class for all linters/stylers/tools"""

    requires_install = []
    base_pyversion = (2, 7, 0)

    def __init__(self):
        self.status_code = 0
        self.hook = None
        self.confpath = None
        self.conf = None

    def add_output_hook(self, func):
        self.hook = func

    def set_config(self, confpath, section):
        self.confpath = confpath
        self.conf = section

    @property
    def name(self):
        return self.__class__.__name__.lower()
