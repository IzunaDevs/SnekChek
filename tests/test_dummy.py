# Stdlib
from unittest import TestCase, skip


class UnitTest(TestCase):
    def test_pass(self):
        self.assertTrue(True)

    @skip("Will always fail")
    def test_fail(self):
        self.assertTrue(False)

    @skip("Will also always fail")
    def test_fail_2(self):
        self.assertTrue(False)
