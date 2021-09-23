import feedparser
import json

master = {}


def get_info(number):
    individual_dict = {}
    link = "https://elearn.memphis.edu/d2l/le/news/rss/" + str(number) + "/course?token=apqblhdwxq9w6o8g11980f"
    parsed = feedparser.parse(link)
    title = parsed['feed']['title'].split(' | ')[0].split(' - ')
    temp = title[0].split('-')
    individual_dict['subject'] = temp[0]
    individual_dict['course'] = temp[1]
    individual_dict['section'] = temp[2]
    individual_dict['id'] = number
    return feedparser.parse(link)['feed']['title']


def parse_links(lower, upper):
    global master
    local = {}
    for number in range(lower, upper + 1):
        print(number)
        local[get_info(number)] = number
    master.update(local)


if __name__ == "__main__":
    globals()
    lower = 8760186
    upper = 8790805
    parse_links(lower, lower + 5)
    with open('newrss.json', 'w') as f:
        json.dump(master, f)
