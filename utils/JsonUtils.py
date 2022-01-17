from core.Course import Course
from core.Professor import Professor
from core.Section import Section


def create_objects(client):
    master_dict = client.master_dict
    create_professor_objects(master_dict["Professors"], client.professors)
    create_course_objects(master_dict["Courses"], client.courses)

def create_professor_objects(master_dict, array):
    print("Generating Professor objects . . . ")
    for value in master_dict:
        title = master_dict[value]["title"]
        email = master_dict[value]["email"]
        office = master_dict[value]["office"]
        prof = Professor(value, title, email, office)
        array.append(prof)
    print(len(array), "Professor objects generated")


def create_course_objects(master_dict, array):
    print("Generating Course objects . . . ")
    for big_key in master_dict:
        code = big_key
        name = master_dict[big_key]["name"]
        hours = master_dict[big_key]["hours"]
        prerequisites = master_dict[big_key]["prerequisites"]
        course_sections = []
        small_key = master_dict[big_key]["sections"]
        for key in small_key:
            section_num = key
            location = small_key[key]["location"]
            instructor = small_key[key]["instructor"]
            days = small_key[key]["days"]
            time = small_key[key]["time"]
            rss = small_key[key]["rss"]
            section = Section(section_num, location, instructor, days, time, rss)
            course_sections.append(section)
        course = Course(code, name, hours, prerequisites, course_sections)
        array.append(course)
    print(len(array), "Course objects generated")

