from Core.Command import Command


class AnnounceCommand(Command):
    def __init__(self):
        self.name = "announce"
        self.help = "Sends a message to the announcement channel"
        self.category = "Moderation"
        self.required_args = 1
        self.required_role = "Community Staff"
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = []

    @staticmethod
    async def execute(event):
        channel = event.get_bot().get_channel(931418786517647360)
        await channel.send(event.get_joined_args())
