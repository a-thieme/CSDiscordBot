from Core.Command import Command
from Core.Database.Queries import update_multiplier


class MultiplierCommand(Command):
    def __init__(self):
        self.name = "multiplier"
        self.help = "Sends a message to the announcement channel"
        self.category = "Moderation"
        self.required_args = 2
        self.required_role = "Community Staff"
        self.owner_command = False
        self.hidden = True
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = []

    @staticmethod
    async def execute(event):
        try:
            to_edit = event.get_message().mentions[0].id
            amount = event.get_args()[1]
            update_multiplier(event.get_database(), to_edit, amount)
            await event.reply_in_dms("Multiplier for user ID: " + str(to_edit) + " has been set to " + amount + ".")
        except IndexError as exc:
            await event.reply("Invalid User")