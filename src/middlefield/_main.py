import functools
import runpy

import toolz

def noop(x):
    """
    Do nothing
    """

entrypoint=toolz.compose(noop,
                         functools.partial(runpy.run_module,
                                           "middlefield",
                                           run_name='__main__'))
