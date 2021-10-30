class Course:
    name = "N/A"
    hours = 0
    prerequisites = []
    sections = []
    rss = []

    def __init__(self, name, hours, prerequisites, sections, rss):
        self.name = name
        self.hours = hours
        self.prerequisites = prerequisites
        self.sections = sections
        self.rss = rss
