import asyncio
import itertools

emojis = ["⏮", "⏪", "⏩", "⏭"]


async def paginate(event, choices):
    message = await event.get_channel().send(embed=choices[0])
    if len(choices) <= 1:
        return
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

    page_num = 1
    while True:
        try:
            reaction, user = await event.get_bot().wait_for('reaction_add', timeout=45.0, check=check_react)
            if str(reaction) == "⏮":
                page_num = 1
            if str(reaction) == "⏭":
                page_num = len(choices)
            if str(reaction) == "⏪" and page_num != 1:
                page_num -= 1
            if str(reaction) == "⏩" and page_num != len(choices):
                page_num += 1
            selection = choices[page_num - 1]
            await message.edit(embed=selection)
            await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            break


def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
