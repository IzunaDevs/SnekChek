u"""Base config for entry points."""

# Stdlib
import os

# Snekchek
import configobj

__all__ = (u"config", )

config = configobj.ConfigObj({  # pylint: disable=invalid-name
    u"all": {
        u"linters": [
            u"flake8", u"pylint", u"yapf", u"isort", u"pyroma", u"safety",
            u"dodgy", u"vulture", u"pytest", u"pypi"
        ]
    },
    u"pypi": {
        u"TWINE_USERNAME": os.environ.get(u"TWINE_USERNAME", u"abc"),
        u"TWINE_PASSWORD": os.environ.get(u"TWINE_PASSWORD", u"abc"),
        u"sign": False,
        u"TWINE_REPOSITORY": u"pypi",
        u"quiet": False
    },
    u"flake8": {
        u"max-line-length": 79,
        u"exclude": [u"build", u"dist"],
        u"ignore": [],
        u"quiet": False
    },
    u"pylint": {
        u"quiet": False
    },
    u"yapf": {
        u"inplace": True,
        u"quiet": False
    },
    u"isort": {
        u"line_length": 79,
        u"multi_line_output": True,
        u"inplace": True,
        u"indent": u"    ",
        u"sections":
        u"FUTURE,STDLIB,THIRDPARTY,FIRSTPARTY,LOCALFOLDER".split(u","),
        u"quiet": False
    },
    u"bandit": {
        u"quiet": False
    },
    u"style": {
        u"inplace": True,
        u"quiet": False
    },
    u"pyroma": {
        u"quiet": False
    },
    u"vulture": {
        u"min-confidence": 60,
        u"verbose": False,
        u"exclude": [],
        u"sort-by-size": False,
        u"quiet": False
    },
    u"safety": {
        u"quiet": False,
        u"ignore": [],
        u"pyup_key": "",
        u"db_pathu": ""
    },
    u"dodgy": {
        u"quiet": False,
        u"ignore_paths": []
    }
})
