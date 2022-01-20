from core.Command import Command


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
    async def execute(message, bot, args, embed):
        professors = bot.professors
        for prof in professors:
            if args[0] in prof.name.lower():
                embed.title = prof.name  # Set embed values
                embed.add_field(name="Title", value=prof.title, inline=False)
                embed.add_field(name="Email", value=prof.email, inline=False)
                embed.add_field(name="Office", value=prof.office, inline=False)
                # adding thumbnail if it can be found
                embed.set_thumbnail(url="https://www.memphis.edu/cs/images/people/" + prof.strip_email() + ".jpg")
                await message.channel.send(embed=embed)
                return
