import datetime

import discord

from Core.Command import Command
from bs4 import BeautifulSoup as bs
import requests as re
import pandas as pd


async def wp_lookup(event):
    search = event.get_joined_args()
    wp = 'https://wp.memphis.edu'
    response = re.get(wp, headers={
        'Host': 'wp.memphis.edu',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    })
    cookies = response.cookies
    res = bs(response.content, 'html.parser')
    params = {x.get('name'): x.get('value') for x in res.find_all('input')}

    response = re.post(
        f'{wp}/search/list',
        {'utf8': params['utf8'], 'authenticity_token': params['authenticity_token'], 'search': search},
        cookies=cookies
    )

    if response.status_code != 200:
        await event.reply_embed_error("Lookup failed due to an HTTP error.")
        return

    try:
        parsed = pd.read_html(response.content.decode('utf-8'))
    except ValueError:
        await event.reply_embed_error(search + " could not be found.")
        return
    if len(parsed) == 0:
        await event.reply_embed_error("Lookup failed due to an HTTP error.")
        return
    else:
        res = parsed[0]
        if len(parsed) == 1:
            tmp = dict(zip([x.strip(':') for x in list(res.get(0).values)], list(res.get(1).values)))
            tmp['Name'] = bs(response.content, 'html.parser').find(id='userinfo').find(id='name').contents[0]
            return tmp
        else:
            return res


class LookupCommand(Command):
    def __init__(self):
        self.name = "lookup"
        self.help = "Looks up a user in banner"
        self.category = "Moderation"
        self.required_args = 1
        self.required_role = "Community Staff"
        self.owner_command = False
        self.hidden = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = []

    @staticmethod
    async def execute(event):
        results = await wp_lookup(event)
        if results is None:
            return
        event.get_embed().title = "Banner Lookup"
        event.get_embed().description = "Looking up " + event.get_joined_args().title() + " in banner"
        if type(results) == dict:
            for key in results:
                event.get_embed().add_field(
                    name=key,
                    value=results[key],
                    inline=True
                )
            await event.send_embed(event.get_embed())
        else:
            choices = []
            for row in results.itertuples(index=False):
                embed = discord.Embed(color=discord.Color.blue())
                embed.title = "Banner Lookup"
                embed.description = "Looking up " + event.get_joined_args().title() + " in banner"
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=event.get_author().name, icon_url=str(event.get_author().avatar))
                for k, v in enumerate(row):
                    if type(v) == str:
                        embed.add_field(
                            name=results.columns.values[k],
                            value=v,
                            inline=True
                        )
                choices.append(embed)
            await event.send_menu(choices)
