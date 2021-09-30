import discord

from core.Command import Command
from utils import JsonUtils


class ProfessorCommand(Command):
    def __init__(self):
        self.name = "professor"
        self.help = "Provides information about a professor"
        self.category = "School"
        self.required_arguments = 1
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["whois", "prof", "teacher"]

    @staticmethod
    async def execute(message, bot, args):
        prof_dict = JsonUtils.get_prof_dict(bot)
        embed_builder = discord.Embed(color=discord.Color.blue())
        for professor in prof_dict:  # Loop through every professor in the dictionary
            if args[0] in professor.lower():  # If the first argument matches any professor names
                embed_builder.title = str(professor).title()
                for field in prof_dict[professor]: # adding email, title, office fields
                    embed_builder.add_field(name=field.title(), value=prof_dict[professor][field], inline=False)
                # todo: automatically generate this and store in new/modified json
                # adding thumbnail if it can be found
                embed_builder.set_thumbnail(url="https://www.memphis.edu/cs/images/people/" + strip_email(prof_dict[professor]["email"]) + ".jpg")
                break  # don't want it to find more than one professor for it
        await message.channel.send(embed=embed_builder)


def strip_email(email):
    username = email.split("@")[0]
    return username.replace(".", "")