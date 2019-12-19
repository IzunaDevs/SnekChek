# __future__ imports
from __future__ import unicode_literals

# Stdlib
import io

# External Libraries
from setuptools import setup, find_packages

# Snekchek
from snekchek import misc
from snekchek.lint import get_linters
from snekchek.secure import get_security
from snekchek.style import get_stylers
from snekchek.tool import get_tools

with io.open("README.rst", encoding="utf-8") as file:
    README = file.read()

with io.open("requirements.txt", encoding="utf-8") as file:
    REQUIREMENTS = file.readlines()

EXTRAS = {}

for group in [get_linters(), get_security(), get_stylers(), get_tools()]:
    for linter in group:
        EXTRAS[linter.__name__.lower()] = linter.requires_install

if __name__ == '__main__':
    setup(
        name="snekchek",
        author="izunadevs",
        author_email="izunadevs@martmists.com",
        maintainer="martmists",
        maintainer_email="mail@martmists.com",
        license="MIT",
        zip_safe=False,
        version=misc.__version__,
        description=misc.description,
        long_description=README,
        url="https://github.com/IzunaDevs/SnekChek",
        packages=find_packages(),
        install_requires=REQUIREMENTS,
        extras_require=EXTRAS,
        entry_points={
            "console_scripts": ["snekchek = snekchek.__main__:main"]
        },
        keywords=[
            "linter",
            "formatter",
            "python",
            "pylint",
            "flake8",
            "isort",
            "vulture",
            "bandit",
            "dodgy",
            "safety",
            "pytest",
            "unittest",
            "pyroma",
            "pypi",
            "yapf",
            "black",
            "snekchek",
            "snekrc",
        ],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: Software Development :: Quality Assurance",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    )
