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

        if "!cs" in message.content:
            process_input(message.content)
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
    splitted = message.split(" ")

    return


def get_prof(name):
    for professor in master_dict["Professors"]:
        if name.lower() in professor.lower():
            for key in master_dict["Professors"][professor]:
                print(master_dict["Professors"][professor][key])


if __name__ == "__main__":
    # import info
    input_file = open("updated.json")
    master_dict = json.load(input_file)

    # start discord bot
    client = MyClient()
    client.run('ODQxODkxMTk2MjA0NjEzNzAy.YJtWRg.KEPdDGnMts7b3EvRnVYIUCVXeI0')

    # testing
    get_prof("Santosh")
