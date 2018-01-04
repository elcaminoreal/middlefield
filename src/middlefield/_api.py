import typing

import caparg as cap
import elcaminoreal
import middlefield
import seashore

COMMANDS = elcaminoreal.Commands()

@COMMANDS.dependency()
def executor(_dependencies, _maybe_dependencies):
    return seashore.Executor(seashore.Shell())

@COMMANDS.command(
    parser=cap.command('',
        requirements=cap.option(type=typing.List[str], have_default=True),
        package=cap.option(type=typing.List[str], have_default=True),
        output=cap.option(type=str, required=True)),
    dependencies=['executor'])
def self_build(args, dependencies):
    package = args['package'].append(f'middlefield={middlefield.__version__}')
    print(package, args['requirements'], args['output'], dependencies)
