import unittest

from middlefield import _main

class NoOpTest(unittest.TestCase):

    def test_noop(self):
        res = _main.noop(["hello"])
        self.assertIsNone(res)
