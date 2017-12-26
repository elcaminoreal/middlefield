import functools
import runpy

import toolz

entrypoint=toolz.compose(lambda x: None,
                         functools.partial(runpy.run_module,
                                           "middlefield",
                                           run_name='__main__'))
