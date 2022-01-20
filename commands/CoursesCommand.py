import re

import discord

from core.Command import Command


class CoursesCommand(Command):
    def __init__(self):
        self.name = "courses"
        self.help = "Lists all core Computer Science courses"
        self.category = "School"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["classes"]

    @staticmethod
    async def execute(message, bot, args, embed):
        name = "COMP"
        if args:  # if not empty
            name = args[0]
        name = name.upper().replace("-", "")
        if re.match(r"([A-z]{3,4})", name) and len(name) <= 4:
            courses = bot.courses
            title = name + " Courses"
            description = "A list of all courses in the " + name +  " subject"
            embed.title = title
            embed.description = description
            field_count = 0
            overflow = discord.Embed(title=title, description=description, color=discord.Color.blue())
            for course in courses:
                if str(course.code).startswith(name):
                    if field_count <= 24:
                        embed.add_field(name=course.code, value=course.name, inline=True)
                    else:
                        overflow.add_field(name=course.code, value=course.name, inline=True)
                    field_count += 1

            await message.channel.send(embed=embed)
            if len(overflow.fields)>0:
                await message.channel.send(embed=overflow)
