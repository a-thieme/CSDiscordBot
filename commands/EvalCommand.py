from core.Command import Command


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
        cursor.execute(" ".join(args))
        myresult = cursor.fetchall()
        await message.channel.send(myresult)
        cursor.close()
