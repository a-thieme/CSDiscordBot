from Core.Command import Command

from Core.Utilities.RankCard import get_rank_card


class RankCommand(Command):
    def __init__(self):
        self.name = "rank"
        self.help = "Checks the level of you or somebody else"
        self.category = "Leveling"
        self.required_args = 0
        self.required_role = None
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 3
        self.aliases = ["level", "xp"]

    @staticmethod
    async def execute(event):
        to_check = event.get_author()
        if event.get_args():
            to_check = event.get_message().mentions[0]
        card = get_rank_card(event, to_check)
        await event.get_channel().send(file=card)
