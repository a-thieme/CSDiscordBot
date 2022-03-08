from Core.Command import Command

class PingCommand(Command):
    def __init__(self):
        self.name = "ping"
        self.help = "Tests discord API latency"
        self.category = "Utility"
        self.required_args = 0
        self.required_role = None
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["testing"]

    @staticmethod
    async def execute(event):
        ping = event.get_bot().latency
        await event.reply(f'Pong! {round(ping, 5)}ms')