import configparser
import json
import os
import sys

from snekchek.baseconfig import config


def flatten(l: list) -> list:
    """ Flattens a list, ignore all the lambdas """
    return list(sorted(filter(lambda y: y is not None,
                              list(map(lambda x: l.extend(x) if isinstance(x, list) else x, l)))))


def get_py_files(dir_name: str) -> list:
    return flatten([x
                    for x in [[f"{path}/{f}"
                               for f in files
                               if f.endswith(".py")]
                              for path, _, files in os.walk(dir_name)
                              if not path.startswith("./build")]
                    if x])


class CheckHandler:
    def __init__(self, check_dir="."):
        self.parser = configparser.ConfigParser()
        self.parser["DEFAULT"] = config

        self.parser.read(".snekrc")
        self.status_code = 0
        self.logs = {}
        self.current = ''

        self.files = get_py_files(check_dir)

    def exit(self):
        for name, log in self.logs.items():
            if self.parser[name].get("quiet"):
                continue

            print(f"[[{name}]]")
            print(json.dumps(log, indent=4))

        sys.exit(self.status_code)

    def run_linter(self, linter):
        self.current = linter.name

        if linter.name not in self.parser["all"]["linters"]:
            return

        linter.add_output_hook(self.out_func)
        linter.run(self.files)
        self.status_code = self.status_code or linter.status_code

    def out_func(self, data):
        self.logs[self.current] = data


class Linter:
    def __init__(self):
        self.status_code = 0
        self.hook = None

    def add_output_hook(self, func):
        self.hook = func

    @property
    def name(self):
        return self.__class__.__name__.lower()
