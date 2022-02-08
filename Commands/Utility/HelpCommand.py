from Core.Command import Command
from Core.Utilities import StringTools


class HelpCommand(Command):
    def __init__(self):
        self.name = "help"
        self.help = "Provides bot help"
        self.category = "Utility"
        self.required_args = 0
        self.required_role = None
        self.owner_command = False
        self.hidden = True
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["commands"]

    @staticmethod
    async def execute(event):
        event.get_embed().title = "Bot Help"
        event.get_embed().description = "List of all commands and their usages"
        all_commands = sorted(event.get_bot().commands, key=lambda cmd: cmd.category)
        for command in all_commands:
            if not command.hidden:
                event.get_embed().add_field(
                    name=command.name.capitalize() + "    " + StringTools.get_formatted_aliases(command),
                    value=command.help,
                    inline=False
                    )
        await event.reply_embed(event.get_embed())
