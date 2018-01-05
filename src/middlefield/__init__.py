"""
Middlefield -- a multi-function build tool
"""

from middlefield._api import COMMANDS, self_build
from middlefield._version import __version__ as _raw_version

__version__ = _raw_version.short()

__all__ = ['COMMANDS', 'self_build', '__version__']
