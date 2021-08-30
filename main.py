import json
import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            # Ignore bot comments
            return

        if message.content == 'ping':
            await message.channel.send('Pong! {0}ms'.format(round(client.latency, 3)))



global master_dict


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
