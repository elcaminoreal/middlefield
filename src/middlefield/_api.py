COMMANDS = elcaminoreal.Commands()

@COMMANDS.command(
    parser=cap.command(''
        requirements=cap.option(type=List[str]),
        package=cap.option(type=List[str]),
        output=cap.option(type=str, required=True)))
def self_build(args, _dependencies):
    pass
