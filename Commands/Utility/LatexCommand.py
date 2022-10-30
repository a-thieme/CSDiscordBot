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
        self.help = """ Tries to print with LaTeX formatting. 
                        Do ?la -r to delete your command if it worked
                        Do \\hbox{test} to write "test" as text. 
                        Otherwise, it is treated like an expression in $$ """
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
        user_inputs = event.get_args()
        remove = False
        if user_inputs[0] == '-r':
            del user_inputs[0]
            remove = True

        buf = '\\\\ \\hbox{-}\\\\'
        results = await do_latex(buf + ''.join(user_inputs).replace('`', '') + buf)
        if results is None:
            return
        await event.send_file(results)
        if remove:
            await event.remove_old_message()
