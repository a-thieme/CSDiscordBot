import discord

from Core.Command import Command
from Core.Utilities import StringTools

import sympy
import time


def do_math(expression, timestamp):
    filename = f'{timestamp}.png'
    sympy.preview(f'${expression}$', output='png', viewer='file', filename=filename)
    return filename


async def do_latex(expression):
    current_time = round(time.time())
    # try:
    filename = do_math(expression, current_time)
    return filename
    # except RuntimeError:
    #     # latex prolly went wrong
    #     return None


class LatexCommand(Command):
    def __init__(self):
        self.name = "la"
        self.help = "Tries to print with LaTeX formatting"
        self.category = "Utility"
        self.required_args = 1
        self.required_role = None
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0

    @staticmethod
    async def execute(event):
        results = await do_latex(''.join(event.get_args()).replace('`', ''))
        if results is None:
            return
        await event.send_file(results)