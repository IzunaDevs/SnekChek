import configparser
import sys

from snekchek.baseconfig import config


class CheckHandler:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser["DEFAULT"] = config

        self.parser.read(".snekrc")
        self.status_code = 0
        self.logs = {}

    def exit(self):
        for name, log in self.logs.items():
            if self.parser[name].get("quiet"):
                continue

            print(log)

        sys.exit(self.status_code)

    def run_linter(self, linter):
        if linter.name not in self.parser["all"]["linters"]:
            return
