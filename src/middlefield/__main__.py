"""
Run command using :code:`middlefield.COMMANDS`
"""

import sys

import elcaminoreal
import middlefield

if __name__ != '__main__':
    raise ImportError("module cannot be imported")

with elcaminoreal.errors_to(sys.stderr):  # pragma: no cover
    middlefield.COMMANDS.run(sys.argv[1:])
