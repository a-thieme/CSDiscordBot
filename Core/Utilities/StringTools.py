# [A-z]{2,4}[0-9]{3,4} for courses
import re


def is_valid_course(input):
    pattern = '^[A-z]{2,4}[0-9]{3,4}$'
    result = re.match(pattern, input)
    if result:
        return True
    else:
        return False


def get_formatted_aliases(command):
    formatted = ""
    for i in range(len(command.aliases)):
        if i == len(command.aliases) - 1:
            formatted += command.aliases[i].capitalize() + ""
        else:
            formatted += command.aliases[i].capitalize() + ", "
    if not formatted:
        return ""
    return "[ *" + formatted + "* ]"
