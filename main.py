import json
import discord
import feedparser
from bs4 import BeautifulSoup

global master_dict
global rss_dict
global admins


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.author.id in admins:
            # if command.isAdmin():
            pass
            # allow admin commands

        if "~cs" in message.content:
            # embed_builder = discord.Embed(color=0x184b91)
            await message.channel.send(embed=process_command(message))


def process_command(message):
    split = message.content.strip().lower().split(" ")
    if len(split) <= 1:
        return error_embed("Expected input but received none")

    embed_builder = discord.Embed(color=discord.Color.blue())
    leading = split[1]

    # Help #
    # print all functions

    # Ping #
    if leading == "ping":
        embed_builder.title = "Check your latency"
        embed_builder.description = 'Pong! {0}ms'.format(round(client.latency, 3))

    # Classes #
    elif leading == "classes":
        embed_builder.title = "Computer Science (Major) Courses"
        embed_builder.description = "A list of the required courses for the CS Major"
        for course in master_dict["Courses"]:
            embed_builder.add_field(name=course, value=master_dict["Courses"][course]['name'], inline=True)

    # Info #
    elif leading == "info":
        name = message.channel.name  # get current channel name
        if len(split) > 2:
            name = split[2]  # if there is an argument, replace the channel name with the argument
        name = name.upper().replace("-", "")  # format all channels to be uppercase in COMP1900 format
        if "COMP" not in name or name not in master_dict["Courses"]:  # find the correct course
            return error_embed("No data is available for this course")
        else:
            return get_class(name, embed_builder)

    elif leading == "professors":
        # header and description
        embed_builder.title = "Computer Science Professors"
        embed_builder.description = "A list of all Full-Time Faculty in the Computer Science Department"

        # adding all the individual professors
        for professor in master_dict["Professors"]:
            embed_builder.add_field(name=professor, value=master_dict["Professors"][professor]["title"], inline=True)

    elif leading == "professor":
        professor_name = message.content.split("professor ")[1].lower()  # grabs everything after "professor "
        return get_professor(professor_name, embed_builder)

    elif leading == "news":
        name = message.channel.name
        if len(split) > 2:
            name = split[2]  # if there is an argument, replace the channel name with the argument
        name = name.upper().replace("-", "")  # format all channels to be uppercase in COMP1900 format
        if name not in rss_dict["RSS"]:
            return error_embed("No data is available for this course")
        else:
            return get_news(name, embed_builder)

    else:
        # input didn't match any of the if/else blocks
        return error_embed("Command invalid")

    # if all went well, this will return the value set by the if/else things
    return embed_builder


def process_admin_command():
    pass


def get_professor(professor_name, embed):
    prof_dict = master_dict["Professors"]
    for professor in prof_dict:
        if professor_name in professor.lower():
            # set title to professor
            embed.title = str(professor).title()
            # adding email, title, office fields
            for field in prof_dict[professor]:
                embed.add_field(name=field.title(), value=prof_dict[professor][field], inline=False)
            # adding thumbnail if it can be found
            # todo: automatically generate this and store in new/modified json
            embed.set_thumbnail(url="https://www.memphis.edu/cs/images/people/" + strip_email(
                master_dict["Professors"][professor]["email"]) + ".jpg")
            # don't want it to find more than one professor for it
            break
    return embed


def get_class(course_name, embed):
    embed.title = course_name.upper()  # + " Info"
    # check for valid class shouldn't be needed because classes are added manually
    # you can only do this because we know the format is COMPXXXX
    temp_dict = master_dict["Courses"][course_name]
    for big_key in temp_dict:
        if big_key == "name":
            embed.description = temp_dict["name"]
        elif big_key == "prerequisites":
            pre_reqs = ""
            for req in temp_dict["prerequisites"]:
                if pre_reqs != "":
                    pre_reqs += ", "
                pre_reqs += req
            embed.add_field(name="Prerequisites", value=pre_reqs, inline=False)
        elif big_key != "sections":
            embed.add_field(name=big_key.title(), value=temp_dict[big_key], inline=False)
        else:
            for section in temp_dict["sections"]:
                string_builder = "```"
                for key in temp_dict["sections"][section]:
                    line = key.title()
                    while len(line) < 13:
                        line += " "
                    line += temp_dict["sections"][section][key] + "\n"
                    string_builder += line
                string_builder += "```"
                embed.add_field(
                    name=section,
                    value=string_builder,
                    inline=False
                )
    return embed


def get_news(course_name, embed):
    embed.title = course_name.upper() + " News"
    key = rss_dict["RSS"][course_name]  # retrieves the rss feed value
    if key == "n/a":
        return error_embed(
            "No news data is available for this course. If you would like to receive news, please contact Adam or Marshall")
    # if the key is available, do stuff
    news = feedparser.parse(
        "https://elearn.memphis.edu/d2l/le/news/rss/" + key + "/course?token=ax72b4q7smuiounj1185cb")
    entries = news.entries
    if len(entries) == 0:
        return error_embed("No news has been recently posted for this course.")
    for entry in entries:
        embed.add_field(name="**" + entry.title + "**", value=strip_text(entry.summary), inline=False)
        strip_text(entry.summary)
    return embed


def strip_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.getText()


def error_embed(description):
    builder = discord.Embed(color=discord.Color.red())
    builder.title = "Error"
    builder.description = description
    return builder


def fix_class_name(name):
    new_name = ""
    temp = name.split('-')
    new_name += temp[0] + temp[1]
    if len(temp) > 2:
        new_name += '-' + temp[2]
    return new_name


def strip_email(email):
    username = email.split("@")[0]
    return username.replace(".", "")


if __name__ == "__main__":
    # import info
    cs_input_file = open("cs_info.json")
    master_dict = json.load(cs_input_file)
    admins = [229392999145144321, 225411938866167808]

    # import rss feeds
    rss_input_file = open("rss.json")
    rss_dict = json.load(rss_input_file)

    # start discord bot
    client = MyClient()
    client.run(open("token.txt", "r").read())
