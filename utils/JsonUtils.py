from core.Professor import Professor


def get_prof_dict(bot):
    return bot.master_dict["Professors"]


def get_course_dict(bot):
    return bot.master_dict["Courses"]


def get_rss_dict(bot):
    return bot.rss_dict["RSS"]


def create_objects(client):
    master_dict = client.master_dict
    create_professor_objects(master_dict["Professors"], client.professors)
    create_course_objects(master_dict["Courses"], client.courses)
    for user_id in master_dict["IDS"]["admin"]:
        client.admins.append(user_id)
    for user_id in master_dict["IDS"]["blacklist"]:
        client.ignored_users.append(user_id)


def create_professor_objects(master_dict, array):
    for value in master_dict:
        title = master_dict[value]["title"]
        email = master_dict[value]["email"]
        office = master_dict[value]["office"]
        prof = Professor(value, title, email, office)
        array.append(prof)


def create_course_objects(master_dict, array):
    pass
