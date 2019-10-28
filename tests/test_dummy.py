# Stdlib
import unittest


def test_dummy():
    assert True


class UnitTest(unittest.TestCase):
    @staticmethod
    def test_pass():
        return False
