import asyncio
import datetime

import discord

emojis = ["⬆️", "✅", "⬇️"]


async def selection(event, choices):
    if len(choices) <= 1:
        return
    embed = discord.Embed(color=discord.Color.blue())
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=event.get_author().name, icon_url=str(event.get_author().avatar_url))
    string_builder = ""
    for value in choices:
        string_builder += ("\n **" + value + "**\n") if value == choices[0] else ("\n" + value + "\n")
    embed.description = string_builder
    message = await event.get_channel().send(embed=embed)
    for reaction in emojis:  #
        await message.add_reaction(reaction)

    def check_react(reaction, user):
        if reaction.message.id != message.id:
            return False
        if user != event.get_author():
            return False
        if str(reaction.emoji) not in emojis:
            return False
        return True

    entry_num = 1
    while True:
        try:
            reaction, user = await event.get_bot().wait_for('reaction_add', timeout=45.0, check=check_react)
            if str(reaction) == "⬆️" and entry_num > 1:
                entry_num -= 1
            if str(reaction) == "✅":
                await message.delete()
                return choices[entry_num - 1]
            if str(reaction) == "⬇️" and entry_num < len(choices):
                entry_num += 1
            string_builder = ""
            for value in choices:
                string_builder += ("\n **" + value + "**\n") if value == choices[entry_num - 1] else (
                            "\n" + value + "\n")
            embed.description = string_builder
            await message.edit(embed=embed)
            await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break
