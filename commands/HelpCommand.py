from core.Command import Command
import discord

from utils import CommandUtils


class HelpCommand(Command):
    def __init__(self):
        self.name = "help"
        self.help = "Provides bot help"
        self.category = "Utility"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["commands", "?"]

    @staticmethod
    async def execute(message, bot, args):
        embed_builder = discord.Embed(color=discord.Color.blue())
        embed_builder.title = "Bot Help"
        embed_builder.description = "List of all commands and their usages"
        all_commands = bot.cmds
        for i in range(len(all_commands)):
            cmd = all_commands[i]
            embed_builder.add_field(name=cmd.name.capitalize() + "    " + CommandUtils.get_formatted_aliases(cmd),
                                    value=cmd.help,
                                    inline=False
                                    )
        await message.channel.send(embed=embed_builder)
