from core.Command import Command


class IgnoreCommand(Command):
    def __init__(self):
        self.name = "ignore"
        self.help = "Blacklists a user from using bot commands"
        self.category = "Moderation"
        self.required_arguments = 1
        self.required_role = "Community Staff"
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["blacklist"]

    @staticmethod
    async def execute(message, bot, args, embed):
        to_be_ignored = message.mentions[0]
        embed.title = "Ignore a user"
        if to_be_ignored.id not in bot.admins:
            bot.ignored_users.append(to_be_ignored.id)
            embed.description = to_be_ignored.name + ' has been blacklisted from using bot commands.'
        else:
            embed.description = "You cannot blacklist an admin."
        await message.channel.send(embed=embed)