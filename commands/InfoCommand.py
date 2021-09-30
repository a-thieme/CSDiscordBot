import discord

from core.Command import Command
from utils import JsonUtils


class InfoCommand(Command):
    def __init__(self):
        self.name = "info"
        self.help = "Provides information on a course"
        self.category = "School"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["course", "class"]

    @staticmethod
    async def execute(message, bot, args):
        course_dict = JsonUtils.get_course_dict(bot)
        embed_builder = discord.Embed(color=discord.Color.blue())
        name = message.channel.name
        if args:
            name = args[0]
        name = name.upper().replace("-", "")
        if "COMP" not in name or name not in course_dict:
            embed_builder.description = "No data is available for this course"
            await message.channel.send(embed=embed_builder)
            return
        await message.channel.send(embed=get_class(name, course_dict, embed_builder))


def get_class(course_name, course_dict, embed):
    embed.title = course_name.upper()  # + " Info"
    # check for valid class shouldn't be needed because classes are added manually
    # you can only do this because we know the format is COMPXXXX
    course_dict = course_dict[course_name]
    for big_key in course_dict:
        if big_key == "name":
            embed.description = course_dict["name"]
        elif big_key == "prerequisites":
            pre_reqs = ""
            for req in course_dict["prerequisites"]:
                if pre_reqs != "":
                    pre_reqs += ", "
                pre_reqs += req
            embed.add_field(name="Prerequisites", value=pre_reqs, inline=False)
        elif big_key != "sections":
            embed.add_field(name=big_key.title(), value=course_dict[big_key], inline=False)
        else:
            for section in course_dict["sections"]:
                string_builder = "```"
                for key in course_dict["sections"][section]:
                    line = key.title()
                    while len(line) < 13:
                        line += " "
                    line += course_dict["sections"][section][key] + "\n"
                    string_builder += line
                string_builder += "```"
                embed.add_field(
                    name=section,
                    value=string_builder,
                    inline=False
                )
    return embed