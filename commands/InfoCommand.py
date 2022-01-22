import asyncio
import re

from core.Command import Command


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
    async def execute(message, bot, args, embed):
        reactemojis = ["⏮", "⏪", "⏩", "⏭"]
        name = message.channel.name
        courses = bot.courses
        if args:  # if not empty
            name = args[0]
        name = name.upper().replace("-", "")
        if re.match(r"([A-z]{3,4}[0-9]{3,4})", name) and len(name)<=8:
            for course in courses:
                if name == course.code:
                    num_of_sections = len(course.sections)
                    has_multiple_sections = True if num_of_sections > 1 else False  # If the course has multiple sections set this boolean to true
                    course_info = get_class_info(course, embed, 0)  # Get the course information
                    msg = await message.channel.send(embed=course_info)
                    if has_multiple_sections:

                        for reaction in reactemojis:  #
                            await msg.add_reaction(reaction)
                        await msg.edit(embed=embed,
                                       content="**Click on the Emotes below to scroll through the Sections for this Course.**")
                        page_num = 1

                        def check_react(reaction, user):
                            if reaction.message.id != msg.id:
                                return False
                            if user != message.author:
                                return False
                            if str(reaction.emoji) not in reactemojis:
                                return False
                            return True

                        while True:
                            try:
                                reaction, user = await bot.wait_for('reaction_add', timeout=45.0, check=check_react)
                                if str(reaction) == "⏮":
                                    page_num = 1
                                if str(reaction) == "⏭":
                                    page_num = num_of_sections
                                if str(reaction) == "⏪" and page_num != 1:
                                    page_num -= 1
                                if str(reaction) == "⏩" and page_num != num_of_sections:
                                    page_num += 1
                                course_info = get_class_info(course, embed, page_num-1)  # Get the course information
                                await msg.edit(embed=course_info)
                                await msg.remove_reaction(reaction, user)
                            except asyncio.TimeoutError:
                                break
                    return
            embed.title = "Error"
            embed.description = "Unable to locate that course."
            await message.channel.send(embed=embed)


def get_section_info(section):
    string_builder = "```"
    string_builder += ("Location     " + section.location + "\n")
    string_builder += ("Instructor   " + section.instructor + "\n")
    string_builder += ("Days         " + str(section.days).replace("nan", "N/A") + "\n")
    string_builder += ("Time         " + section.time)
    string_builder += "```"
    return string_builder


def get_class_info(course, embed, index):
    embed.clear_fields()
    section = course.sections[index]
    embed.title = course.code.upper() + " [" + section.section_num + "] INFO"
    embed.description = course.name
    embed.add_field(name="Credit Hours", value=course.hours, inline=False)
    if course.prerequisites:  # if not empty
        pre_reqs = ""
        for req in course.prerequisites:
            if pre_reqs != "":
                pre_reqs += ", "
            pre_reqs += req
        embed.add_field(name="Prerequisites", value=pre_reqs, inline=False)
    embed.add_field(name=section.section_num, value=get_section_info(section), inline=False)
    return embed
