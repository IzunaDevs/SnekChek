# __future__ imports
from __future__ import print_function, unicode_literals

# Stdlib
import os
import sys

# External Libraries
import configobj

if sys.version_info < (3, 0, 0):
    input = raw_input  # noqa pylint: disable=all


class ConfigGenerator:
    """class for config generation"""
    def get_tools(self):
        """Lets the user enter the tools he want to use"""
        tools = "flake8,pylint,vulture,pyroma,isort,yapf,black,safety,dodgy,pytest,pypi".split(
            ",")
        print("Available tools: {0}".format(",".join(tools)))
        answer = ask_list("What tools would you like to use?",
                          ["flake8", "pytest"])

        if any(tool not in tools for tool in answer):
            print("Invalid answer, retry.")
            self.get_tools()
        return answer

    def flake8(self):
        """Configuring flake8"""
        pass

    def pylint(self):
        """Configuring pylint, will do nothing"""
        pass

    def vulture(self):
        """Configuring vulture"""
        pass

    def pyroma(self):
        """Configuring pyroma"""
        pass

    def isort(self):
        """Configuring isort"""
        pass

    def yapf(self):
        """Configuring yapf"""
        pass

    def safety(self):
        """Configuring safety"""
        pass

    def dodgy(self):
        """Configuring dodgy"""
        pass

    def pytest(self):
        """Configuring pytest"""
        pass

    def pypi(self):
        """Configuring pypi"""
        pass

    def main(self):
        """The main function for generating the config file"""
        path = ask_path("where should the config be stored?", ".snekrc")

        conf = configobj.ConfigObj()

        tools = self.get_tools()
        for tool in tools:
            conf[tool] = getattr(self, tool)()  # pylint: disable=assignment-from-no-return
        conf.filename = path
        conf.write()

        print("Written config file!")

        if "pylint" in tools:
            print(
                "Please also run `pylint --generate-rcfile` to complete setup")


def ask_bool(question, default=True):
    """Asks a question yes no style"""
    default_q = "Y/n" if default else "y/N"
    answer = input("{0} [{1}]: ".format(question, default_q))
    lower = answer.lower()
    if not lower:
        return default
    return lower == "y"


def ask_int(question, default=None):
    """Asks for a number in a question"""
    default_q = (" [default: {0}]: ".format(default)
                 if default is not None else '')
    answer = input("{0} [{1}]: ".format(question, default_q))

    if not answer:
        if default is None:
            print("No default set, try again.")
            return ask_int(question, default)
        return default

    if any(x not in "1234567890" for x in answer):
        print("Please enter only numbers (0-9).")
        return ask_int(question, default)

    return int(answer)


def ask_path(question, default=None):
    """Asks for a path"""
    default_q = (" [default: {0}]: ".format(default)
                 if default is not None else '')
    answer = input("{0} [{1}]: ".format(question, default_q))

    if answer == '':
        return default

    if os.path.isdir(answer):
        return answer

    print(
        "No such directory: {answer}, please try again".format(answer=answer))
    return ask_path(question, default)


def ask_list(question, default=None):
    """Asks for a comma seperated list of strings"""
    default_q = (" [default: {0}]: ".format(",".join(default))
                 if default is not None else '')
    answer = input("{0} [{1}]: ".format(question, default_q))

    if answer == '':
        return default
    return [ans.strip() for ans in answer.split(",")]


def ask_str(question, default=None):
    """Asks for a simple string"""
    default_q = (" [default: {0}]: ".format(default)
                 if default is not None else '')
    answer = input("{0} [{1}]: ".format(question, default_q))

    if answer == '':
        return default
    return answer


def generate():
    generator = ConfigGenerator()
    generator.main()
