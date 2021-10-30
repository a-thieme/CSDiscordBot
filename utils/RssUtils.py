from discord.ext import tasks


@tasks.loop(seconds=10)  # repeat after every 10 seconds
async def check_for_news():
    print("x")
