import datetime

import discord

from Core.Command import Command
from Core.Database.Queries import get_professors, get_professor_sections
from Core.Utilities import StringTools


class ProfessorCommand(Command):
    def __init__(self):
        self.name = "professor"
        self.help = "Provides information about a professor"
        self.category = "School"
        self.required_args = 1
        self.required_role = None
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["whois", "prof", "instructor"]

    @staticmethod
    async def execute(event):
        looking_for = event.get_joined_args()
        located_professors = get_professors(event.get_database(), looking_for)
        if not located_professors:
            await event.reply_embed_error("That professor could not be located", 3)
            return
        choices = []
        fields = ["Name", "Title", "Email", "Phone Number", "Office"]
        for professor in located_professors:
            embed = discord.Embed(color=discord.Color.blue())
            embed.title = professor[0]
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=event.get_author().name, icon_url=str(event.get_author().avatar))
            if professor[5] is not None:  # If they have an associated image
                embed.set_thumbnail(url=professor[5])
            for attribute in range(1, 5):  # Since we only want Title, Email, Phone Number, and Office
                if professor[attribute] is not None:
                    embed.add_field(name=fields[attribute], value=professor[attribute], inline=False)
            sections = get_professor_sections(event.get_database(), professor[0])
            for sec in sections:
                embed.add_field(name=(sec[0] + str(sec[1])), value=StringTools.get_professor_section_info(sec), inline=False)
            choices.append(embed)
        await event.send_menu(choices)


