# [A-z]{2,4}[0-9]{3,4} for courses
import re


def is_valid_course(input):
    pattern = '^[A-z]{2,4}[0-9]{3,4}$'
    result = re.match(pattern, input)
    if result:
        return True
    else:
        return False
