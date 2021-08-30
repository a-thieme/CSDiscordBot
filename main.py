import json
import discord

global master_dict


class MyClient(discord.Client):
    bot_indicator = "!cs"

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            # Ignore bot comments
            return

        if "!cs" in message.content:
            process_input(message.content)
        if message.content == 'ping':
            await message.channel.send('Pong! {0}ms'.format(round(client.latency, 3)))


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
    client.run('ODQxODkxMTk2MjA0NjEzNzAy.YJtWRg.O7fSXIonBDCKgy5ASSUel9Nr1KQ')

    # testing
    get_prof("Santosh")
