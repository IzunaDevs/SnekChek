__all__ = ("config",)

config = {
    "all": {
        "linters": ["flake8", "pylint", "yapf", "isort", "pyroma",
                    "safety", "bandit", "dodgy", "pydocstyle",
                    "vulture", "pytest", "pypi"]
    },
    "pypi": {
        "TWINE_USERNAME": os.environ.get("TWINE_USERNAME", "abc"),
        "TWINE_PASSWORD": os.environ.get("TWINE_PASSWORD", "abc")
    }
    "flake8": {
    },
    "pylint": {
    },
    "yapf": {
    },
}
