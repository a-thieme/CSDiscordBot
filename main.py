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
        self.commands = [TestCommand(), RankCommand(), LeaderboardCommand(), ClassesCommand(), ProfessorCommand()]

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


def main():
    client = Client()
    client.run(open("token.txt", "r").read())


main()
