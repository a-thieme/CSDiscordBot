from Core.Command import Command


class TestCommand(Command):
    def __init__(self):
        self.name = "test"
        self.help = "Tests bot response"
        self.category = "Utility"
        self.required_args = 0
        self.required_role = None
        self.owner_command = True
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 10
        self.aliases = ["testing"]

    @staticmethod
    async def execute(event):
        # choices = ["001 - Kriangsiri Malasri [MW 11:20am-12:45pm] <t:1644713529:R>", "002 - Kriangsiri Malasri [TR 11:20am-12:45pm] <t:1644713529:R>", "003 - Fatih Sen [MW 11:20am-12:45pm] <t:1644713529:R>", "004 - Kriangsiri Malasri [MW 4:40pm-16:45pm] <t:1644713529:R>"]
        # await event.reply(("selection result was ", await event.send_selection_menu(choices)))
        await event.reply("Test")
