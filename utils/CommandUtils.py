def get_formatted_aliases(command):
    formatted = ""
    for i in range(len(command.aliases)):
        if i == len(command.aliases)-1:
            formatted += command.aliases[i].capitalize() + ""
        else:
            formatted += command.aliases[i].capitalize() + ", "
    return formatted

