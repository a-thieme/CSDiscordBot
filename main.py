import discord
import mysql.connector
from mysql.connector import errorcode

from Commands import *
from Core.Command.CommandEvent import CommandEvent
from Core.Database.Config import db_config


class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = None
        self.commands = [TestCommand(), RankCommand(), LeaderboardCommand(), ClassesCommand(), ProfessorCommand(),
                         AnnounceCommand(), HelpCommand(), MultiplierCommand(), CourseCommand(), PingCommand(),
                         LookupCommand(), LatexCommand()]

    async def on_ready(self):
        self.connect_database()
        await self.change_presence(status=discord.Status.online, activity=discord.Game("with sloths"))
        print('Logged on as', self.user)
        if self.database.is_connected():
            print("Connection established to database")

    def connect_database(self):
        try:
            print("Connecting to Database . . . ")
            self.database = mysql.connector.connect(**db_config)
        except mysql.connector.Error as exc:
            if exc.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid credentials.")
            else:
                print(exc)

    async def on_message(self, message):
        command_event = CommandEvent(self, message)
        await command_event.filter_commands()

    # new user verification for WiC
    async def on_member_join(self, member):
        dm_channel = member.create_dm()
        await dm_channel.send("""Welcome to the Memphis CS Discord Server!
        If you would like to join the Women in Computing channel, please send your UID (the one with numbers).
        We do not store it anywhere.
        If you aren't automatically added, DM either Marshall or Adam who will help you out.""")


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = Client(intents=intents)

    # there's probably a better way to do this, but it works alright
    try:
        # python is run by bot user
        token = open("token.txt", 'r').read()
    except FileNotFoundError:
        # python is run by root user (system service)
        token = open("/home/bot/csbot/token.txt", 'r').read()

    client.run(token)


main()
