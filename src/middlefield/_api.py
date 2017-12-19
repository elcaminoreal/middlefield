COMMANDS = elcaminoreal.Commands()

@COMMANDS.command(
    name='self-build',
    parser=cap.command(
        requirements=cap.option(type=List[str]),
        package=cap.option(type=List[str]),
        output=cap.option(type=str, required=True),
    ),
)
def self_build(requirements, package, output):
    # ...
    # write pex

def run(args, environment):
    return COMMANDS.run(args, environment)
