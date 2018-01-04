import elcaminoreal
import caparg as cap
import typing

COMMANDS = elcaminoreal.Commands()

@COMMANDS.command(
    parser=cap.command('',
        requirements=cap.option(type=typing.List[str], have_default=True),
        package=cap.option(type=typing.List[str], have_default=True),
        output=cap.option(type=str, required=True)))
def self_build(args, _dependencies):
    print(args, _dependencies)
