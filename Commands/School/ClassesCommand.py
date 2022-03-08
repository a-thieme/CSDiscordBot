import datetime
import discord

from Core.Command import Command
from Core.Database.Queries import get_courses
from Core.Utilities.Paginator import grouper


class ClassesCommand(Command):
    def __init__(self):
        self.name = "classes"
        self.help = "List all courses in a subject"
        self.category = "School"
        self.required_args = 1
        self.required_role = None
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["courses"]

    @staticmethod
    async def execute(event):
        subject = event.get_args()[0].upper()
        located_courses = get_courses(event.get_database(), subject)
        if not located_courses:
            await event.reply_embed_error("That subject could not be located", 3)
            return
        choices = []
        for group in grouper(24, located_courses):
            embed = discord.Embed(color=discord.Color.blue())
            embed.title = subject + " Courses"
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=event.get_author().name, icon_url=str(event.get_author().avatar))
            embed.description = "A list of courses in the " + subject + " subject"
            for course in group:
                course_title = (course[0].upper() + str(course[1]))
                embed.add_field(name=course_title, value=course[3], inline=True)
            choices.append(embed)
        await event.send_menu(choices)


