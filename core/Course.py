import main


def get_dict():
    return main.MyClient.master_dict["Courses"]


class Course:
    name = "N/A"
    hours = 0
    prerequisites = []
    sections = []
