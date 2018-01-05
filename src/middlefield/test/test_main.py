"""
Test main entry point
"""

import unittest

from middlefield import _main


# pylint: disable=assignment-from-none
class NoOpTest(unittest.TestCase):

    """
    Tests for noop
    """

    def test_noop(self):
        """
        noop returns None
        """
        res = _main.noop(["hello"])
        self.assertIsNone(res)
# pylint: enable=assignment-from-none
