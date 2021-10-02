from core.Command import Command
from utils import CommandUtils


class AnnounceCommand(Command):
    def __init__(self):
        self.name = "announce"
        self.help = "Announces a message to the server"
        self.category = "Utility"
        self.required_arguments = 0
        self.required_role = "Community Staff"
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = []

    @staticmethod
    async def execute(message, bot, args):
        announcements = bot.get_channel(748159572283490406)  # announcements channel
        args = CommandUtils.join_args(args)
        await announcements.send(args)
