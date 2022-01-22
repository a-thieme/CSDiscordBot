from core.Command import Command
from table2ascii import table2ascii as t2a, PresetStyle
import mysql.connector


class EvalCommand(Command):
    def __init__(self):
        self.name = "eval"
        self.help = "Executes a SQL query"
        self.category = "Utility"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = True
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["sql", "execute"]

    @staticmethod
    async def execute(message, bot, args, embed):
        cursor = bot.conn.cursor()
        try:
            cursor.execute(" ".join(args))
            query_result = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            field_values = [i for i in query_result]
            output = t2a(header=field_names, body=field_values, style=PresetStyle.thin_compact)
            await message.channel.send(f"```\n{output}\n```")
        except mysql.connector.Error as err:
            await message.channel.send("Something went wrong: {}".format(err))
        cursor.close()
