import discord

from core.Command import Command


class TestCommand(Command):
    def __init__(self):
        self.name = "test"
        self.help = "Tests bot response"
        self.category = "Utility"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = True
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["testing"]

    @staticmethod
    async def execute(message, bot, args):
        embed_builder = discord.Embed(color=discord.Color.blue())
        embed_builder.title = "Bot testing"
        embed_builder.description = 'Generic testing'
        await message.channel.send(embed=embed_builder)
