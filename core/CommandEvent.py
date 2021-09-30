import discord


class CommandEvent:
    def __init__(self, message, command, arguments, bot):
        self.message = message
        self.command = command
        self.arguments = arguments
        self.bot = bot

    async def execute_checks(self):
        embed_builder = discord.Embed(color=discord.Color.blue())
        if len(self.arguments) < self.command.required_arguments:
            embed_builder.description = "Not enough arguments, expected " + str(self.command.required_arguments)
            await self.message.channel.send(embed=embed_builder)
            return # argument check
        if self.command.mod_command and (self.message.author.id != 225411938866167808 or 229392999145144321):
            embed_builder.description = "You don't have permission to use this command"
            await self.message.channel.send(embed=embed_builder)
            return #mod command check
        await self.command.execute(self.message, self.bot, self.arguments)
