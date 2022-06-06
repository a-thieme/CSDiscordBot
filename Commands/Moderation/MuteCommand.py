from Core.Command import Command
import datetime
import requests


def timeout_user(*, user_id: int, guild_id: int, until: int):
    endpoint = f'guilds/{guild_id}/members/{user_id}'
    headers = {"Authorization": f"Bot {TOKEN}"}
    url = 'https://discord.com/api/v9/' + endpoint
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=time_in_mins)).isoformat()
    json = {'communication_disabled_until': timeout}
    session = requests.patch(url, json=json, headers=headers)
    if session.status_code in range(200, 299):
        return session.json()
    else:
        return print("Did not find any\n", session.status_code)


class MuteCommand(Command):
    def __init__(self):
        self.name = "mute"
        self.help = "Times user out"
        self.category = "Moderation"
        self.required_args = 1
        self.required_role = "Community Staff"
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ['timeout']

    @staticmethod
    async def execute(event):
        try:
            user = event.get_message().mentions[0].id
            timeout_user(user_id=user)
        except IndexError:
            'do nothing lol'
