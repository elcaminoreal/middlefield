import contextlib
import os
import typing
import shutil
import tempfile

import caparg as cap
import elcaminoreal
import middlefield
from pex import pex_builder
import seashore

COMMANDS = elcaminoreal.Commands()

@COMMANDS.dependency()
def executor(_dependencies, _maybe_dependencies):
    return seashore.Executor(seashore.Shell())

@contextlib.contextmanager
def tmpdir():
    ret = tempfile.mkdtemp()
    try:
        yield ret
    finally:
        shutil.rmtree(ret)

@COMMANDS.command(
    parser=cap.command('',
        requirements=cap.option(type=typing.List[str], have_default=True),
        package=cap.option(type=typing.List[str], have_default=True),
        output=cap.option(type=str, required=True)),
    dependencies=['executor'])
def self_build(args, dependencies):
    package = list(args['package'])
    package.append(f'middlefield=={middlefield.__version__}')
    requirements = list(args['requirements'])
    output = args['output']
    xctor = dependencies['executor']
    builder = pex_builder.PEXBuilder()
    builder.set_entry_point('middlefield')
    with tmpdir() as wheelhouse:
        xctor.pip.wheel(*list(package),
                        requirements=requirements, wheel_dir=wheelhouse).batch()
        for dist in os.listdir(wheelhouse):
            print("Adding", dist)
            dist = os.path.join(wheelhouse, dist)
            builder.add_dist_location(dist)
        builder.build(output)
