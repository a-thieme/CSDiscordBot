import json

import discord
from discord import DMChannel

from commands import *
from core import CommandEvent
from utils import JsonUtils
from utils.CommandUtils import find_command


class CSBot(discord.Client):
    cmds = [PingCommand(), TestCommand(), HelpCommand(), ProfessorCommand(), FacultyCommand(), InfoCommand(),
            CoursesCommand(), NewsCommand(), AnnounceCommand(), ShutdownCommand(), IgnoreCommand()]
    courses = []
    professors = []
    admins = []
    ignored_users = []
    cs_input_file = open("cs_info.json")
    master_dict = json.load(cs_input_file)
    rss_input_file = open("rss.json")
    rss_dict = json.load(rss_input_file)

    async def on_ready(self):
        JsonUtils.create_objects(self)
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if isinstance(message.channel, DMChannel):
            return
        if message.content.lower().startswith("#cs "):
            args = message.content.lower().replace("#cs ", "", 1).split(" ")
            cmd = args[0]
            args.pop(0)
            locate_command = find_command(cmd, self)
            embed = discord.Embed(color=discord.Color.blue())
            if isinstance(locate_command, AnnounceCommand):
                args = message.content.split(" ")
            if locate_command is not None:
                cmd_event = CommandEvent(message, locate_command, args, self, embed)
                await cmd_event.execute_checks()
            else:
                embed.description = "No command found"
                await message.channel.send(embed=embed)


def main():  # main method
    client = CSBot()
    client.run(open("token.txt", "r").read())


main()  # call main
