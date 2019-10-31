# Stdlib
from unittest import TestCase, skip


class UnitTest(TestCase):
    def test_pass(self):
        self.assertTrue(True)

    @skip("Will always fail")
    def test_fail(self):
        self.assertTrue(False)
