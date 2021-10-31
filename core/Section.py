class Section:
    section_num = ""
    location = ""
    instructor = ""
    days = ""
    time = ""
    rss = []

    def __init__(self, section_num, location, instructor, days, time, rss):
        self.section_num = section_num
        self.location = location
        self.instructor = instructor
        self.days = days
        self.time = time
        self.rss = rss

    def __str__(self):
        return self.section_num + "\t(" + self.location + ")\nInstructor: " + self.instructor + "\nDay/Time: " + self.days + " at " + self.time + "\nRss: " + str(self.rss) + "\n\n"
