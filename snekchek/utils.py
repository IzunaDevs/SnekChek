"""
This module provides redirect_* functions for Python <3.5
"""

# Stdlib
from contextlib import contextmanager
import sys


@contextmanager
def redirect_stdout(new):
    old = sys.stdout
    sys.stdout = new
    yield
    sys.stdout = old


@contextmanager
def redirect_stderr(new):
    old = sys.stderr
    sys.stderr = new
    yield
    sys.stderr = old
