def get_formatted_aliases(command):
    formatted = ""
    for i in range(len(command.aliases)):
        if i == len(command.aliases)-1:
            formatted += command.aliases[i].capitalize() + ""
        else:
            formatted += command.aliases[i].capitalize() + ", "
    if not formatted:
        return ""
    return "[ *" + formatted + "* ]"


def join_args(args):
    return " ".join(args)


def find_command(cmd_input, bot):
    for i in range(len(bot.cmds)):
        if bot.cmds[i].name.lower() == cmd_input.lower() or cmd_input.lower() in bot.cmds[i].aliases:
            return bot.cmds[i]
    return None

