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
        name = message.channel.name
        courses = bot.courses
        if args:  # if not empty
            name = args[0]
        name = name.upper().replace("-", "")
        for course in courses:
            if name == course.code:
                await message.channel.send(embed=get_class_info(course, embed))
                return
        embed.title = name.upper() + " Info"
        embed.description = "Unable to locate that course."
        await message.channel.send(embed=embed)


def get_class_info(course, embed):
    embed.title = course.code.upper() + " Info"
    embed.description = course.name
    embed.add_field(name="Credit Hours", value=course.hours, inline=False)
    if course.prerequisites:  # if not empty
        pre_reqs = ""
        for req in course.prerequisites:
            if pre_reqs != "":
                pre_reqs += ", "
            pre_reqs += req
        embed.add_field(name="Prerequisites", value=pre_reqs, inline=False)
    for section in course.sections:
        string_builder = "```"
        string_builder += ("Location     " + section.location + "\n")
        string_builder += ("Instructor   " + section.instructor + "\n")
        string_builder += ("Days         " + section.days + "\n")
        string_builder += ("Time         " + section.time)
        string_builder += "```"
        embed.add_field(name=section.section_num, value=string_builder, inline=False)
    return embed
