# [A-z]{2,4}[0-9]{3,4} for courses
import re


def is_valid_course(input):
    pattern = '^([A-z]{2,4})([0-9]{3,4})$'
    result = re.match(pattern, input)
    if result and len(input) <= 8:
        groups = result.groups()
        return True, groups[0], groups[1]
    else:
        return False, None, None


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


def get_professor_section_info(section):
    section = [str(i or 'N/A') for i in section]
    string_builder = "```"
    string_builder += ("Course         " + section[0] + str(section[1]) + "\n")
    string_builder += ("Days           " + section[3] + "\n")
    string_builder += ("Time           " + section[4] + "\n")
    string_builder += "```"
    return string_builder


def get_course_section_info(section):
    string_builder = "```"
    string_builder += ("Location     " + section[6] + "\n")
    string_builder += ("Instructor   " + section[20] + "\n")
    string_builder += ("Days         " + str(section[5]).replace("None", "N/A") + "\n")
    string_builder += ("Time         " + section[4])
    string_builder += "```"
    return string_builder