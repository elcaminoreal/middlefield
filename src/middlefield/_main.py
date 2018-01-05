"""
A setup-friendly entrypoint, running __main__
"""

import functools
import runpy

import toolz


def noop(_dummy):
    """
    Do nothing
    """
    return None


# pylint: disable=invalid-name
entrypoint = toolz.compose(noop,
                           functools.partial(runpy.run_module,
                                             "middlefield",
                                             run_name='__main__'))
# pylint: enable=invalid-name
