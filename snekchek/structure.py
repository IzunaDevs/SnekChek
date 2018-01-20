""" Common classes and utility functions. """

# Stdlib
import configparser
import json
import os
import sys

# Snekchek
from snekchek.baseconfig import config
import snekchek.format


def flatten(nested_list: list) -> list:
    """ Flattens a list, ignore all the lambdas. """
    return list(sorted(filter(lambda y: y is not None,
                              list(map(lambda x: (nested_list.extend(x)  # noqa: T484
                                                  if isinstance(x, list) else x),
                                       nested_list)))))


def get_py_files(dir_name: str) -> list:
    return flatten([x
                    for x in [[f"{path}/{f}"
                               for f in files
                               if f.endswith(".py")]
                              for path, _, files in os.walk(dir_name)
                              if not path.startswith("./build")]
                    if x])


class CheckHandler:
    def __init__(self, file, out_json, check_dir="."):
        self.parser = configparser.ConfigParser()
        self.parser.update(config)

        self.parser.read(file)
        self.fn = file  # pylint: disable=invalid-name
        self.status_code = 0
        self.logs = {}
        self.current = ''
        self.json = out_json

        self.indent = 4 if "--debug" in sys.argv else None

        self.files = get_py_files(check_dir)

    def exit(self):
        total = sum(len(logs) for logs in self.logs.values())
        if self.json:
            self.logs['total'] = total
            print(json.dumps(self.logs, indent=self.indent))

        else:
            for name, log in self.logs.items():
                if not log or self.parser[name].get("quiet"):
                    continue

                print(f"[[{name}]]")
                getattr(snekchek.format, name + "_format")(log)
                print("\n")

            print("-" * 30)
            print("Total:", total)

        sys.exit(self.status_code)

    def run_linter(self, linter):
        self.current = linter.name

        if linter.name not in self.parser["all"]["linters"]:
            return

        linter.add_output_hook(self.out_func)
        linter.set_config(self.fn, self.parser[linter.name])
        linter.run(self.files)
        self.status_code = self.status_code or linter.status_code

    def out_func(self, data):
        self.logs[self.current] = data


class Linter:
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
