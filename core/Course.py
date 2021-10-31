class Course:
    code = ""
    name = ""
    hours = 0
    prerequisites = []
    sections = []

    def __init__(self, code, name, hours, prerequisites, sections):
        self.code = code
        self.name = name
        self.hours = hours
        self.prerequisites = prerequisites
        self.sections = sections

    def print_sections(self):
        string = ""
        for sec in self.sections:
            string += str(sec)
        return string

    def __str__(self):
        return self.code + "\t(" + self.name + ")\nHours: " + self.hours + "\nPrerequisites: " + str(self.prerequisites) + "\nSections: \n" + self.print_sections()
