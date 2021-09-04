import json
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
    