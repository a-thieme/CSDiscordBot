import datetime

import discord

from Core.Command import Command
from Core.Database.Queries import get_section
from Core.Utilities import StringTools


class CourseCommand(Command):
    def __init__(self):
        self.name = "course"
        self.help = "Provides information on a specific course"
        self.category = "School"
        self.required_args = 0
        self.required_role = None
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["info", "class"]

    @staticmethod
    async def execute(event):
        course = event.get_channel().name
        if event.get_args():
            course = event.get_args()[0]
        valid_format, subject, code = StringTools.is_valid_course(course.replace("-", ""))
        if valid_format:
            located_sections = get_section(event.get_database(), subject, code)
            if not located_sections:
                await event.reply_embed_error("Unable to locate that course")
                return
            choices = []
            for section in located_sections:
                embed = discord.Embed(color=discord.Color.blue())
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=event.get_author().name, icon_url=str(event.get_author().avatar))
                embed.title = course.upper() + " [" + section[3] + "] INFO"
                embed.description = section[18]
                embed.add_field(name="Credit Hours", value=section[17], inline=False)
                embed.add_field(name=section[3], value=StringTools.get_course_section_info(section), inline=False)
                choices.append(embed)
            await event.send_menu(choices)
            return
        await event.reply_embed_error("Unable to locate that course")
