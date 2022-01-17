import feedparser
from bs4 import BeautifulSoup

from core.Command import Command
from utils import JsonUtils


def strip_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.getText()


def get_news(course, embed):
    embed.title = course.code.upper() + " News"
    section = course.sections[0]  # TODO currently we only pull news from section 001, other sections get ignored.
    key = section.rss["id"]  # retrieves the rss feed value
    token = section.rss["token"]
    if key == "N/A":
        embed.description = "No news data is available for this course. If you would like to receive news, please contact Adam or Marshall"
        return embed
    news = feedparser.parse(
        "https://elearn.memphis.edu/d2l/le/news/rss/" + key + "/course?token=" + token)
    entries = news.entries
    if len(entries) == 0:
        embed.description = "No news has been recently posted for this course."
        return embed
    for entry in entries:
        num_of_fields = len(entry) // 1024 + 1
        for i in range(num_of_fields):
            embed.add_field(name="**" + entry.title + "**", value=strip_text(entry.summary[i*1024:i+1*1024]), inline=False)
    return embed

class NewsCommand(Command):
    def __init__(self):
        self.name = "news"
        self.help = "Pulls news data from ecourseware"
        self.category = "School"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["updates", "newsfeed"]

    @staticmethod
    async def execute(message, bot, args, embed):
        name = message.channel.name
        courses = bot.courses
        if args:  # if not empty
            name = args[0]
        name = name.upper().replace("-", "")
        for course in courses:
            if name == course.code:
                await message.channel.send(embed=get_news(course, embed))
                return
        embed.title = name.upper() + " Newsfeed"
        embed.description = "Unable to locate that course."
        await message.channel.send(embed=embed)
