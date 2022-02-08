import asyncio
import datetime
import time

import discord
from discord import DMChannel

from Core.Database.Queries import get_last_message, increase_xp, update_msg_time
from Core.Utilities.Paginator import paginate


class CommandEvent:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.args = message.content.replace('#', '', 1).split(" ")
        embed_builder = discord.Embed(color=discord.Color.blue())
        embed_builder.timestamp = datetime.datetime.utcnow()
        embed_builder.set_footer(text=self.message.author.name, icon_url=str(self.message.author.avatar_url))
        self.embed = embed_builder

    async def filter_commands(self):
        message = self.message
        if message.author.bot or message.author == self.bot.user:
            return
        if isinstance(message.channel, DMChannel):
            return
        if message.content.startswith('#'):
            self.command = self.locate_command(self.args[0])
            passes_requirements = await self.filter_requirements()
            if self.command and passes_requirements:
                await self.command.execute(self)
                update_msg_time(self.get_database(), message)
            return
        increase_xp(self.get_database(), message)

    async def filter_requirements(self):
        if self.command is None:
            return False
        args = self.args[1:]
        ### Arguments ###
        if len(args) < self.command.required_args:
            await self.reply_embed_error("Not enough arguments, expected " + str(self.command.required_args))
            return False
        ### Owner Command ###
        if self.command.owner_command and self.message.author.id not in [225411938866167808, 229392999145144321]:
            await self.reply_embed_error("This command is only for bot admins")
            return False
        ### Cooldown ###
        if self.command.cooldown > 0:
            last_msg = get_last_message(self.bot.database, self.message.author.id)
            msg_time_unix = time.mktime(self.message.created_at.timetuple())
            cooldown = msg_time_unix - last_msg
            if cooldown < self.command.cooldown:
                await self.reply_embed_error("This command is on cooldown")
                return False
        ### Required Role ###
        if self.command.required_role is not None:
            role = discord.utils.find(lambda r: r.name == self.command.required_role, self.message.guild.roles)
            if role not in self.message.author.roles:
                await self.reply_embed_error("You don't have permission to use this command")
                return False

        return True

    # ██╗   ██╗████████╗██╗██╗     ███████╗
    # ██║   ██║╚══██╔══╝██║██║     ██╔════╝
    # ██║   ██║   ██║   ██║██║     ███████╗
    # ██║   ██║   ██║   ██║██║     ╚════██║
    # ╚██████╔╝   ██║   ██║███████╗███████║
    # ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝

    def get_author(self):
        return self.message.author

    def get_message(self):
        return self.message

    def get_channel(self):
        return self.message.channel

    def get_guild(self):
        return self.message.guild

    def get_bot(self):
        return self.bot

    def get_args(self):
        return self.args[1:]

    def get_joined_args(self):
        return ' '.join(self.args[1:])

    def get_embed(self):
        return self.embed

    def get_database(self):
        return self.bot.database

    async def get_user_by_id(self, user_id):
        return await self.bot.fetch_user(int(user_id))

    async def reply(self, content):
        await self.message.channel.send(content)

    async def reply_embed(self, content):
        await self.message.channel.send(embed=content)

    async def reply_in_dms(self, content):
        await self.message.author.send(content)

    async def reply_embed_in_dms(self, content):
        self.embed.description = content
        await self.message.author.send(embed=self.embed)

    async def reply_error(self, content, seconds=5):
        await self.message.channel.send(content, delete_after=seconds)

    async def reply_embed_error(self, content, seconds=5):
        self.embed.description = content
        await self.message.channel.send(embed=self.embed, delete_after=seconds)

    async def send_menu(self, choices):
        await paginate(self, choices)

    def locate_command(self, to_find):
        to_find = to_find.lower()
        for cmd in self.bot.commands:
            if cmd.name == to_find or to_find in cmd.aliases:
                return cmd
        return None
