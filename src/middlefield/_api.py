import elcaminoreal
import caparg as cap
import typing

COMMANDS = elcaminoreal.Commands()

@COMMANDS.command(
    parser=cap.command('',
        requirements=cap.option(type=typing.List[str]),
        package=cap.option(type=typing.List[str]),
        output=cap.option(type=str, required=True)))
def self_build(args, _dependencies):
    pass
