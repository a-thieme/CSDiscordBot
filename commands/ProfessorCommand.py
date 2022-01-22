import asyncio

import mysql.connector

from core.Command import Command


class ProfessorCommand(Command):
    def __init__(self):
        self.name = "professor"
        self.help = "Provides information about a professor"
        self.category = "School"
        self.required_arguments = 1
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["whois", "prof", "teacher"]

    @staticmethod
    async def execute(message, bot, args, embed):
        reactemojis = ["⏮", "⏪", "⏩", "⏭"]
        cursor = bot.conn.cursor()
        name = " ".join(args)
        try:
            cursor.execute('SELECT * FROM instructor WHERE name LIKE %s', [f"%{name}%"])
            query_result = cursor.fetchall()
            if not query_result:
                embed.title = "Error"
                embed.description = "No professors matching that input were located."
                await message.channel.send(embed=embed)
                return
            num_of_professors = len(query_result)
            multiple_results = True if num_of_professors > 1 else False
            professor_info = get_professor_info(query_result[0], embed, cursor)  # Get the professor information
            msg = await message.channel.send(embed=professor_info)
            if multiple_results:

                for reaction in reactemojis:  #
                    await msg.add_reaction(reaction)
                await msg.edit(embed=embed,
                               content="**Click on the Emotes below to scroll through Professors matching the name" + name + ".**")
                page_num = 1

                def check_react(reaction, user):
                    if reaction.message.id != msg.id:
                        return False
                    if user != message.author:
                        return False
                    if str(reaction.emoji) not in reactemojis:
                        return False
                    return True

                while True:
                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=45.0, check=check_react)
                        if str(reaction) == "⏮":
                            page_num = 1
                        if str(reaction) == "⏭":
                            page_num = num_of_professors
                        if str(reaction) == "⏪" and page_num != 1:
                            page_num -= 1
                        if str(reaction) == "⏩" and page_num != num_of_professors:
                            page_num += 1
                        professor_info = get_professor_info(query_result[page_num - 1], embed,
                                                            cursor)  # Get the professor information
                        await msg.edit(embed=professor_info)
                        await msg.remove_reaction(reaction, user)
                    except asyncio.TimeoutError:
                        break
        except mysql.connector.Error as err:
            await message.channel.send("Something went wrong: {}".format(err))
        cursor.close()


def get_section_info(section):
    section = [str(i or 'N/A') for i in section]
    string_builder = "```"
    string_builder += ("Course         " + section[0] + str(section[1]) + "\n")
    string_builder += ("Days           " + section[3] + "\n")
    string_builder += ("Time           " + section[4] + "\n")
    string_builder += "```"
    return string_builder


def get_professor_info(professor, embed, cursor):
    name = professor[0]
    embed.clear_fields()
    field_names = [i[0] for i in cursor.description]
    embed.title = name
    if professor[5] is not None:
        embed.set_thumbnail(url=professor[5])
    i = 1
    for value in professor:
        if value is not None and 1 < i < 5:
            print(str(i) + " = " + value)
            embed.add_field(name=str(field_names[i-1]).title(), value=value, inline=False)
        i += 1
    # basic professor information added, now add sections
    cursor.execute('SELECT subj, num, sec_num, days, time FROM taught_by AS teaches JOIN section AS sec WHERE '
                   'instructor LIKE %s AND teaches.crn=sec.crn', [f"%{name}%"])
    query_result = cursor.fetchall()
    if query_result:
        for result in query_result:
            embed.add_field(name=result[2], value=get_section_info(result), inline=False)
    return embed
