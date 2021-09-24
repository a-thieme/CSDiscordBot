import feedparser
import json
import threading

master = {}


def get_info(number):
    individual_dict = {}
    link = "https://elearn.memphis.edu/d2l/le/news/rss/" + str(number) + "/course?token=apqblhdwxq9w6o8g11980f"
    parsed = feedparser.parse(link)
    if 'feed' not in parsed or 'title' not in parsed['feed']:
        return False
    title = parsed['feed']['title'].split(' | ')[0].split(' - ')
    if title == ['The University of Memphis']:
        return False
    if len(title) > 1:
        individual_dict['title'] = title[1]
    temp = title[0].split('-')
    individual_dict['subject'] = temp[0]
    individual_dict['course_num'] = temp[1]
    individual_dict['section'] = temp[2]
    individual_dict['RSS_ID'] = number
    # returns subject, course, section number, dict with title, section, RSS_ID
    return individual_dict


def parse_links(lower, upper):
    global master
    for number in range(lower, upper + 1):
        # print(number)
        info = get_info(number)
        if not info:
            print(number)
            continue

        subject = info['subject']
        if subject not in master:
            master[subject] = {}

        course_num = info['course_num']
        if course_num not in master[subject]:
            master[subject][course_num] = {}

        if 'title' not in master[subject][course_num] and 'title' in info:
            master[subject][course_num]['title'] = info['title']

        section = info['section']
        if section not in master[subject][course_num]:
            master[subject][course_num][section] = {}
        master[subject][course_num][info['section']]['RSS_ID'] = info['RSS_ID']


if __name__ == "__main__":
    globals()
    lower = 8760186
    lowmid = 8767841
    middle = 8775496
    uppermid = 8783151
    upper = 8790805
    # print(get_info(8760262))
    # t1 = threading.Thread(target=parse_links(lower, lowmid))
    # t2 = threading.Thread(target=parse_links(lowmid, middle))
    # t3 = threading.Thread(target=parse_links(middle, uppermid))
    # t4 = threading.Thread(target=parse_links(uppermid, upper + 1))
    #
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    #
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()

    parse_links(lower, upper + 1)
    with open('newrss.json', 'w') as f:
        # f.writelines(json.dumps(master))
        json.dump(master, f)

