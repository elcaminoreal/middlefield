"""
Middlefield's main API
"""

import contextlib
import os
import typing
import shutil
import tempfile

from caparg import command, option
import elcaminoreal
from pex import pex_builder
import seashore

from middlefield import _version

COMMANDS = elcaminoreal.Commands()


@COMMANDS.dependency()
def executor(_dependencies, _maybe_dependencies):
    """
    Return an executor
    """
    return seashore.Executor(seashore.Shell())


@COMMANDS.dependency(name='pex_builder')
def get_pex_builder(_dependencies, _maybe_dependencies):
    """
    Return a Pex builder
    """
    return pex_builder.PEXBuilder


@contextlib.contextmanager
def tmpdir():
    """
    Context manager creating a temporary directory
    """
    ret = tempfile.mkdtemp()
    try:
        yield ret
    finally:
        shutil.rmtree(ret)


@COMMANDS.command(parser=command('',
                                 requirements=option(type=typing.List[str],
                                                     have_default=True),
                                 package=option(type=typing.List[str],
                                                have_default=True),
                                 shebang=option(type=str),
                                 output=option(type=str, required=True)),
                  dependencies=['executor', 'pex_builder'])
def self_build(args, dependencies):
    """
    Build middlefield, together with any plugins, into a Pex file
    """
    package = list(args['package'])
    my_version = _version.__version__.short()
    package.append('middlefield=={}'.format(my_version))
    requirements = list(args['requirements'])
    output = args['output']
    xctor = dependencies['executor']
    builder = dependencies['pex_builder']()
    builder.set_entry_point('middlefield')
    if 'shebang' in args:
        builder.set_shebang(args['shebang'])
    with tmpdir() as wheelhouse:
        xctor.pip.wheel(*list(package),
                        requirements=requirements,
                        wheel_dir=wheelhouse).batch()
        for dist in os.listdir(wheelhouse):
            dist = os.path.join(wheelhouse, dist)
            builder.add_dist_location(dist)
        builder.build(output)
