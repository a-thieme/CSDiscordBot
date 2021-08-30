import json
import discord

global master_dict


class MyClient(discord.Client):
    bot_indicator = "!cs"

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if "~cs" in message.content:
            await message.channel.send(process_input(message))
        if message.content == 'ping':
            await message.channel.send('Pong! {0}ms'.format(round(client.latency, 3)))


def process_input(message):
    split = message.content.strip().lower().split(" ")
    leading = split[1]
    if leading == "info":
        if len(split) == 2:
            return "length is 2"
    #        cs info
    elif leading == "classes":
        course_message = discord.Embed(title="Computer Science (Major) Courses", description="A list of the required courses for the CS Major", color=0x184b91)
        for course in master_dict["Courses"]:
            for courseinfo in master_dict["Courses"]:
                course_message.add_field(name=course, value=master_dict["Courses"][course]['name'], inline=True)
                return course_message
    elif leading == "professors":
        return "leading is professors"

    return "error happened"


def get_prof(name):
    for professor in master_dict["Professors"]:
        if name.lower() in professor.lower():
            for key in master_dict["Professors"][professor]:
                print(master_dict["Professors"][professor][key])


def reformat_class_name(name):
    new_name = ""
    temp = name.split('-')
    new_name += temp[0] + temp[1]
    if len(temp) > 2:
        new_name += '-' + temp[2]
    return new_name


def get_class(class_name):
    return "something"


if __name__ == "__main__":
    # import info
    input_file = open("updated.json")
    master_dict = json.load(input_file)

    # start discord bot
    client = MyClient()
    client.run(open("token.txt", "r").read())
    