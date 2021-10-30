from core.Command import Command


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
    async def execute(message, bot, args, embed):
        professors = bot.professors
        embed.title = "Computer Science Professors"
        embed.description = "A list of all Full-Time Faculty in the Computer Science Department"
        for professor in professors:  # adding all the individual professors
            embed.add_field(name=professor.name, value="[" + professor.title + "](https://www.memphis.edu/cs/people/faculty_pages/" + professor.get_web_name() + ".php)", inline=True)
        await message.channel.send(embed=embed)
