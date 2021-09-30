import discord

from core.Command import Command
from utils import JsonUtils


class FacultyCommand(Command):
    def __init__(self):
        self.name = "faculty"
        self.help = "Lists all full-time department faculty"
        self.category = "School"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["professors", "staff"]

    @staticmethod
    async def execute(message, bot, args):
        prof_dict = JsonUtils.get_prof_dict(bot)
        embed_builder = discord.Embed(color=discord.Color.blue())
        embed_builder.title = "Computer Science Professors"
        embed_builder.description = "A list of all Full-Time Faculty in the Computer Science Department"
        for professor in prof_dict: # adding all the individual professors
            embed_builder.add_field(name=professor, value=prof_dict[professor]["title"], inline=True)
        await message.channel.send(embed=embed_builder)