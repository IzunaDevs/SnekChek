import configparser
import sys

from snekchek.baseconfig import config


class CheckHandler:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser["DEFAULT"] = config

        # Only when baseconfig is done, run this once to create example .snekrc
        # with open(".snekrc.example") as f:
        #     self.parser.write(f)
        self.parser.read(".snekrc")
        self.status_code = 0
        self.logs = {}

    def exit(self):
        for name, log in logs.items():
            if self.parser[name].get("quiet"):
                continue

            print(log)

        sys.exit(self.status_code)

    def run_lint(self, linter):
        if linter.name not in self.parser["all"]["linters"]:
            return

    def run_style(self, linter):
        if linter.name not in self.parser["all"]["linters"]:
            return

    def run_secure(self, linter):
        if linter.name not in self.parser["all"]["linters"]:
            return
