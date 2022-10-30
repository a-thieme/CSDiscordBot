import discord

from Core.Command import Command
from Core.Utilities import StringTools

import sympy
import time


def do_math(expression, timestamp):
    filename = f'/tmp/{timestamp}.png'
    try:
        # unix
        sympy.preview(f'${expression}$', output='png', viewer='file', filename=filename)
    except FileNotFoundError:
        # windows
        filename = f'c:/temp/{timestamp}.png'
        sympy.preview(f'${expression}$', output='png', viewer='file', filename=filename)

    return filename


async def do_latex(expression):
    current_time = round(time.time())
    try:
        filename = do_math(expression, current_time)
        return filename
    except RuntimeError:
        # latex prolly went wrong
        return None


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
        self.aliases = ['```latex']

    @staticmethod
    async def execute(event):
        buf = '\\\\ \\hbox{-}\\\\'
        results = await do_latex(buf + ''.join(event.get_args()).replace('`', '') + buf)
        if results is None:
            return
        await event.send_file(results)
        await event.remove_old_message()
