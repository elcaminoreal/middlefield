"""
Run command using :code:`middlefield.COMMANDS`
"""

import sys

import middlefield

if __name__ != '__main__':
    raise ImportError("module cannot be imported")

middlefield.COMMANDS.run(sys.argv[1:])  # pragma: no cover
