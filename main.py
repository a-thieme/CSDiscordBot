import json
import re
import discord

global master_dict


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if "~cs" in message.content:
            embedBuilder = discord.Embed(color=0x184b91)
            await message.channel.send(embed=process_input(message, embedBuilder))

def process_input(message, embedBuilder):
    split = message.content.strip().lower().split(" ")
    if len(split)<=1:
        embedBuilder.title = "Error"
        embedBuilder.description = "Expected input but received none"
        embedBuilder.color = 0xFF0000
        return embedBuilder
    leading = split[1]
    ###### Ping
    if leading == "ping":
        embedBuilder.title = "Check your latency"
        embedBuilder.description = 'Pong! {0}ms'.format(round(client.latency, 3))
        return embedBuilder
    ###### Classes
    if leading == "classes":
        embedBuilder.title = "Computer Science (Major) Courses"
        embedBuilder.description = "A list of the required courses for the CS Major"
        for course in master_dict["Courses"]:
            embedBuilder.add_field(name=course, value=master_dict["Courses"][course]['name'], inline=True)
        return embedBuilder
    ###### Info
    if leading == "info":
        if len(split) > 2:
            return "length is 2 or more (an course argument was given)"
    #        cs info

        return "length is 1 (no args)"
    elif leading == "professors":
        embedBuilder.title = "Computer Science Professors"
        embedBuilder.description = "A list of all Full-Time Faculty in the Computer Science Department"
        for professor in master_dict["Professors"]:
            embedBuilder.add_field(name=professor, value=master_dict["Professors"][professor]["title"], inline=True)
        return embedBuilder
    elif leading == "professor":
        professor_name = message.content.split("professor ")[1]
        for professor in master_dict["Professors"]:
            if professor_name.lower() in professor.lower():
                embedBuilder.title = professor_name.title()
                embedBuilder.add_field(name="Email", value=master_dict["Professors"][professor]["email"], inline=False)
                embedBuilder.add_field(name="Title", value=master_dict["Professors"][professor]["title"], inline=False)
                embedBuilder.add_field(name="Office", value=master_dict["Professors"][professor]["office"], inline=False)
                embedBuilder.set_thumbnail(url="https://www.memphis.edu/cs/images/people/" + strip_email(master_dict["Professors"][professor]["email"]) + ".jpg")
        return embedBuilder

    embedBuilder.title = "Error"
    embedBuilder.description = "Command invalid"
    embedBuilder.color = 0xFF0000
    return embedBuilder

def reformat_class_name(name):
    new_name = ""
    temp = name.split('-')
    new_name += temp[0] + temp[1]
    if len(temp) > 2:
        new_name += '-' + temp[2]
    return new_name

def strip_email(email):
    return email.split("@")[0]

def get_class(class_name):
    return "something"


if __name__ == "__main__":
    # import info
    input_file = open("updated.json")
    master_dict = json.load(input_file)

    # start discord bot
    client = MyClient()
    client.run(open("token.txt", "r").read())
    