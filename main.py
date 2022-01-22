import json

import discord
import mysql.connector
from discord import DMChannel

from commands import *
from core import CommandEvent
from utils import JsonUtils, Database
from utils.CommandUtils import find_command


class CSBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmds = [PingCommand(), TestCommand(), HelpCommand(), ProfessorCommand(), FacultyCommand(),
                     InfoCommand(),
                     CoursesCommand(), NewsCommand(), AnnounceCommand(), ShutdownCommand(), IgnoreCommand(),
                     EvalCommand()]
        self.conn = None
    courses = []
    professors = []
    cs_input_file = open("cs_info.json")
    master_dict = json.load(cs_input_file)

    async def on_ready(self):
        if self.conn.is_connected():
            print("Connection established to database")
        JsonUtils.create_objects(self)
        await self.change_presence(status=discord.Status.online, activity=discord.Game("with sloths"))
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if isinstance(message.channel, DMChannel):
            return
        if message.content.startswith("?") and not message.content.endswith("?"):
            args = message.content.lower().replace("?", "", 1).split(" ")
            cmd = args[0]
            args.pop(0)
            locate_command = find_command(cmd, self)
            embed = discord.Embed(color=discord.Color.blue())
            if locate_command is not None:
                cmd_event = CommandEvent(message, locate_command, args, self, embed)
                await cmd_event.execute_checks()


def main():  # main method
    client = CSBot()
    client.conn = Database.get_connection()
    client.run(open("token.txt", "r").read())


main()  # call main
