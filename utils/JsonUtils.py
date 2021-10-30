from core.Professor import Professor


def get_prof_dict(bot):
    return bot.master_dict["Professors"]


def get_course_dict(bot):
    return bot.master_dict["Courses"]


def get_rss_dict(bot):
    return bot.rss_dict["RSS"]


def create_professor_objects(master_dict, array):
    for value in master_dict:
        title = master_dict[value]["title"]
        email = master_dict[value]["email"]
        office = master_dict[value]["office"]
        prof = Professor(value, title, email, office)
        array.append(prof)



