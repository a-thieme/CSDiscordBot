import json

import discord
from discord import DMChannel

from commands.CoursesCommand import CoursesCommand
from commands.FacultyCommand import FacultyCommand
from commands.HelpCommand import HelpCommand
from commands.InfoCommand import InfoCommand
from commands.NewsCommand import NewsCommand
from commands.ProfessorCommand import ProfessorCommand
from commands.TestCommand import TestCommand
from commands.PingCommand import PingCommand
from core.CommandEvent import CommandEvent


class MyClient(discord.Client):
    cmds = [PingCommand(), TestCommand(), HelpCommand(), ProfessorCommand(), FacultyCommand(), InfoCommand(), CoursesCommand(), NewsCommand()]
    cs_input_file = open("cs_info.json")
    master_dict = json.load(cs_input_file)
    rss_input_file = open("rss.json")
    rss_dict = json.load(rss_input_file)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if isinstance(message.channel, DMChannel):
            return
        message.content = message.content.lower()
        if message.content.startswith("~cs "):
            args = message.content.replace("~cs ", "", 1).split(" ")
            cmd = args[0]
            args.pop(0)
            locate_command = find_command(cmd, self)
            if locate_command is not None:
                cmd_event = CommandEvent(message, locate_command, args, self)
                await cmd_event.execute_checks()
            else:
                embed_builder = discord.Embed(color=discord.Color.blue())
                embed_builder.description = "No command found"
                await message.channel.send(embed=embed_builder)


def main():  # main method
    client = MyClient()
    client.run(open("token.txt", "r").read())


def find_command(cmd_input, bot):
    for i in range(len(bot.cmds)):
        if bot.cmds[i].name.lower() == cmd_input.lower() or cmd_input.lower() in bot.cmds[i].aliases:
            return bot.cmds[i]
            break
    return None


main()  # call main
