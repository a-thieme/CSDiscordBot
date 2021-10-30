from core.Command import Command


class PingCommand(Command):
    def __init__(self):
        self.name = "ping"
        self.help = "Checks your latency"
        self.category = "Utility"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["latency"]

    @staticmethod
    async def execute(message, bot, args, embed):
        embed.title = "Check your latency"
        embed.description = 'Pong! {0}ms'.format(round(bot.latency, 3))
        await message.channel.send(embed=embed)
