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
            process_input(message)
        if message.content == 'ping':
            await message.channel.send('Pong! {0}ms'.format(round(client.latency, 3)))
        if message.content == '~classes':
            course_message = discord.Embed(title="Computer Science (Major) Courses", description="A list of the required courses for the CS Major", color=0x184b91)
            for course in master_dict["Courses"]:
                course_message.add_field(name=course, value="Value1", inline=True)
                for courseinfo in master_dict["Courses"]:
                    print(courseinfo[0])
            await message.channel.send(embed=course_message)


def process_input(message):
    split = message.content.strip().lower().split(" ")
    leading = split[1]
    if leading == "info":
        if len(split) == 2:
            message.channel.send("length is 2")
    #        cs info
    elif leading == "classes":
        message.channel.send("leading is classes")

    elif leading == "professors":
        message.channel.send("leading is professors")

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
    client.run('ODQxODkxMTk2MjA0NjEzNzAy.YJtWRg.KEPdDGnMts7b3EvRnVYIUCVXeI0')

    # testing
    get_prof("Santosh")
