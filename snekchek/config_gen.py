# __future__ imports
from __future__ import print_function

# Stdlib
import os
import sys

# External Libraries
import configobj

if sys.version_info < (3, 0, 0):
    input = raw_input  # noqa pylint: disable=all


class ConfigGenerator:
    u"""class for config generation"""
    def get_tools(self):
        u"""Lets the user enter the tools he want to use"""
        tools = u"flake8,pylint,vulture,pyroma,isort,yapf,safety,dodgy,pytest,pypi".split(
            u",")
        print(u"Available tools: {0}".format(u",".join(tools)))
        answer = ask_list(u"What tools would you like to use?",
                          [u"flake8", u"pytest"])

        if any(tool not in tools for tool in answer):
            print(u"Invalid answer, retry.")
            self.get_tools()
        return answer

    def flake8(self):
        u"""Configuring flake8"""
        pass

    def pylint(self):
        u"""Configuring pylint, will do nothing"""
        pass

    def vulture(self):
        u"""Configuring vulture"""
        pass

    def pyroma(self):
        u"""Configuring pyroma"""
        pass

    def isort(self):
        u"""Configuring isort"""
        pass

    def yapf(self):
        u"""Configuring yapf"""
        pass

    def safety(self):
        u"""Configuring safety"""
        pass

    def dodgy(self):
        u"""Configuring dodgy"""
        pass

    def pytest(self):
        u"""Configuring pytest"""
        pass

    def pypi(self):
        u"""Configuring pypi"""
        pass

    def main(self):
        u"""The main function for generating the config file"""
        path = ask_path(u"where should the config be stored?", u".snekrc")

        conf = configobj.ConfigObj()

        tools = self.get_tools()
        for tool in tools:
            conf[tool] = getattr(self, tool)()  # pylint: disable=assignment-from-no-return
        conf.filename = path
        conf.write()

        print(u"Written config file!")

        if u"pylint" in tools:
            print(
                u"Please also run `pylint --generate-rcfile` to complete setup"
            )


def ask_bool(question, default=True):
    u"""Asks a question yes no style"""
    default_q = u"Y/n" if default else u"y/N"
    answer = input(u"{0} [{1}]: ".format(question, default_q))
    lower = answer.lower()
    if not lower:
        return default
    return lower == u"y"


def ask_int(question, default=None):
    u"""Asks for a number in a question"""
    default_q = u" [default: {0}]: ".format(
        default) if default is not None else ''
    answer = input(u"{0} [{1}]: ".format(question, default_q))

    if not answer:
        if default is None:
            print(u"No default set, try again.")
            return ask_int(question, default)
        return default

    if any(x not in u"1234567890" for x in answer):
        print(u"Please enter only numbers (0-9).")
        return ask_int(question, default)

    return int(answer)


def ask_path(question, default=None):
    u"""Asks for a path"""
    default_q = u" [default: {0}]: ".format(
        default) if default is not None else ''
    answer = input(u"{0} [{1}]: ".format(question, default_q))

    if answer == '':
        return default

    if os.path.isdir(answer):
        return answer

    print(
        u"No such directory: {answer}, please try again".format(answer=answer))
    return ask_path(question, default)


def ask_list(question, default=None):
    u"""Asks for a comma seperated list of strings"""
    default_q = u" [default: {0}]: ".format(
        u",".join(default)) if default is not None else ''
    answer = input(u"{0} [{1}]: ".format(question, default_q))

    if answer == '':
        return default
    return [ans.strip() for ans in answer.split(u",")]


def ask_str(question, default=None):
    u"""Asks for a simple string"""
    default_q = u" [default: {0}]: ".format(
        default) if default is not None else ''
    answer = input(u"{0} [{1}]: ".format(question, default_q))

    if answer == '':
        return default
    return answer


def generate():
    generator = ConfigGenerator()
    generator.main()
