from core.Command import Command


class ShutdownCommand(Command):
    def __init__(self):
        self.name = "shutdown"
        self.help = "Softly terminates the bot"
        self.category = "Utility"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = True
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["terminate", "disconnect", "quit"]

    @staticmethod
    async def execute(message, bot, args, embed):
        embed.title = "Disconnect"
        embed.description = 'CS Bot will now shut down.'
        await message.channel.send(embed=embed)
        await bot.close()
