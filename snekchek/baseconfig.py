# Stdlib
import os

# External Libraries
import configobj

__all__ = ("config",)

config = configobj.ConfigObj({  # pylint: disable=invalid-name
    "all": {
        "linters": ["flake8", "pylint", "yapf", "isort", "pyroma",
                    "safety", "bandit", "dodgy", "pydocstyle",
                    "vulture", "pytest", "pypi"]
    },
    "pypi": {
        "TWINE_USERNAME": os.environ.get("TWINE_USERNAME", "abc"),
        "TWINE_PASSWORD": os.environ.get("TWINE_PASSWORD", "abc")
    },
    "flake8": {
        "max-line-length": 79,
        "exclude": ["build", "dist"],
        "ignore": ["D100", "D101"]
    },
    "pylint": {
    },
    "yapf": {
    },
    "isort": {
        "line_length": 79,
        "inplace": 'false',
        "indent": '    '
    },
    "bandit": {
    },
    "mypy": {
    },
    "pyroma": {
    },
    "vulture": {
        "min-confidence": 60,
        "verbose": False,
        "exclude": [],
        "sort-by-size": False
    }
})
