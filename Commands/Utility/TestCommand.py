from Core.Command import Command


class TestCommand(Command):
    def __init__(self):
        self.name = "test"
        self.help = "Tests bot response"
        self.category = "Utility"
        self.required_args = 0
        self.required_role = None
        self.owner_command = True
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 10
        self.aliases = ["testing"]

    @staticmethod
    async def execute(event):
        await event.reply("hello")
