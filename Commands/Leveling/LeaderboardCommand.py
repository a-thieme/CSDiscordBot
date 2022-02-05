from Core.Command import Command
from Core.Utilities.RankCard import get_leaderboard_card


class LeaderboardCommand(Command):
    def __init__(self):
        self.name = "leaderboard"
        self.help = "Displays an XP leaderboard for the top ten users"
        self.category = "Leveling"
        self.required_args = 0
        self.required_role = None
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 3
        self.aliases = ["lb", "ranks", "levels"]

    @staticmethod
    async def execute(event):
        leaderboard = await get_leaderboard_card(event)
        await event.get_channel().send(leaderboard)
