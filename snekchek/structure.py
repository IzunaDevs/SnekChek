""" Common classes and utility functions. """

# Stdlib
import json
import os
import re
import subprocess  # noqa: B404
import sys

# External Libraries
import snekchek.format


def flatten(nested_list: list) -> list:
    """Flattens a list, ignore all the lambdas."""
    return list(sorted(filter(lambda y: y is not None,
                              list(map(lambda x: (nested_list.extend(x)  # noqa: T484
                                                  if isinstance(x, list) else x),
                                       nested_list)))))


def get_py_files(dir_name: str) -> list:
    """Get all .py files."""
    return flatten([
        x for x in
        [["{0}/{1}".format(path, f) for f in files if f.endswith(".py")]
         for path, _, files in os.walk(dir_name)
         if not path.startswith("./build")] if x
    ])


class ModuleNotInstalled(Exception):
    pass


class CheckHandler:
    def __init__(self, file: str, out_json: bool, check_dir: str = "."):
        # Do this here so setup.py doesn't error
        from snekchek.baseconfig import config
        import configobj

        self.parser = config
        self.parser.merge(configobj.ConfigObj(file))

        self.fn = file  # pylint: disable=invalid-name
        self.status_code = 0
        self.logs = {}
        self.current = ''
        self.json = out_json

        self.indent = 4 if "--debug" in sys.argv else None

        self.files = get_py_files(check_dir)

        patt = re.compile(r"(?P<package>\S+) \((?P<version>\S+)\)", re.M)

        proc = subprocess.Popen(  # noqa: B603
            [sys.executable, "-m", "pip", "list"],
            stdout=subprocess.PIPE)

        proc.wait()

        matches = list(patt.finditer(proc.stdout.read().decode()))

        self.installed = [p.group("package") for p in matches]

    def exit(self) -> None:
        """Raise SystemExit with correct status code and output logs."""
        total = sum(len(logs) for logs in self.logs.values())
        if self.json:
            self.logs['total'] = total
            print(json.dumps(self.logs, indent=self.indent))

        else:
            for name, log in self.logs.items():
                if not log or self.parser[name].as_bool("quiet"):
                    continue

                print("[[{0}]]".format(name))
                getattr(snekchek.format, name + "_format")(log)
                print("\n")

            print("-" * 30)
            print("Total:", total)

        sys.exit(self.status_code)

    def run_linter(self, linter) -> None:
        """Run a checker class"""
        self.current = linter.name

        if (linter.name not in self.parser["all"].as_list("linters")
                or linter.base_pyversion > sys.version_info):  # noqa: W503
            return

        if any(x not in self.installed for x in linter.requires_install):
            raise ModuleNotInstalled(linter.requires_install)

        linter.add_output_hook(self.out_func)
        linter.set_config(self.fn, self.parser[linter.name])
        linter.run(self.files)
        self.status_code = self.status_code or linter.status_code

    def out_func(self, data) -> None:
        self.logs[self.current] = data


class Linter:
    """Common shared class for all linters/stylers/tools"""

    requires_install = []
    base_pyversion = (3, 0, 0)

    def __init__(self):
        self.status_code = 0
        self.hook = None
        self.confpath = None
        self.conf = None

    def add_output_hook(self, func) -> None:
        self.hook = func

    def set_config(self, confpath: str, section) -> None:
        self.confpath = confpath
        self.conf = section

    @property
    def name(self):
        return self.__class__.__name__.lower()
