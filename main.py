import json
import discord

global master_dict


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if "~cs" in message.content:
            # embedBuilder = discord.Embed(color=0x184b91)
            await message.channel.send(embed=process_input(message))


def process_input(message):
    split = message.content.strip().lower().split(" ")
    if len(split) <= 1:
        return error_embed("Expected input but received none")

    embed_builder = discord.Embed(color=discord.Color.blue())
    leading = split[1]
    # Ping #
    if leading == "ping":
        embed_builder.title = "Check your latency"
        embed_builder.description = 'Pong! {0}ms'.format(round(client.latency, 3))
    # Classes #
    elif leading == "classes":
        embed_builder.title = "Computer Science (Major) Courses"
        embed_builder.description = "A list of the required courses for the CS Major"
        for course in master_dict["Courses"]:
            embed_builder.add_field(name=course, value=master_dict["Courses"][course]['name'], inline=True)
    # Info #
    elif leading == "info":
        # course argument was given
        if len(split) > 2:
            return "length is 2 or more (an course argument was given)"
        # just info
        # check if channel is in comp
        name = ""
        name = message.channel.name
        if "comp" not in name:
            embed_builder.title = "Invalid channel"
        else:
            embed_builder.title = name
        # return "length is 1 (no args)"
    elif leading == "professors":

        embed_builder.title = "Computer Science Professors"
        embed_builder.description = "A list of all Full-Time Faculty in the Computer Science Department"

        for professor in master_dict["Professors"]:
            embed_builder.add_field(name=professor, value=master_dict["Professors"][professor]["title"], inline=True)

    elif leading == "professor":
        professor_name = message.content.split("professor ")[1].lower()
        # find
        for professor in master_dict["Professors"]:
            if professor_name in professor.lower():
                # set title to professor
                embed_builder.title = professor_name.title()
                # adding email, title, office fields
                embed_builder.add_field(name="Email", value=master_dict["Professors"][professor]["email"], inline=False)
                embed_builder.add_field(name="Title", value=master_dict["Professors"][professor]["title"], inline=False)
                embed_builder.add_field(name="Office", value=master_dict["Professors"][professor]["office"],
                                        inline=False)
                # adding thumbnail if it can be found
                # todo: automatically generate this and store in new/modified json
                embed_builder.set_thumbnail(url="https://www.memphis.edu/cs/images/people/" + strip_email(
                    master_dict["Professors"][professor]["email"]) + ".jpg")

                # don't want it to find more than one professor for it
                break
    else:
        # input didn't match any of the if/else blocks
        return error_embed("Command invalid")

    # if all went well, this will return the value set by the if/else things
    return embed_builder


def error_embed(description):
    builder = discord.Embed(color=discord.Color.red())
    builder.title = "Error"
    builder.description = description
    return builder


def reformat_class_name(name):
    new_name = ""
    temp = name.split('-')
    new_name += temp[0] + temp[1]
    if len(temp) > 2:
        new_name += '-' + temp[2]
    return new_name


def strip_email(email):
    return email.split("@")[0]


def get_class(class_name):
    return "something"


if __name__ == "__main__":
    # import info
    input_file = open("updated.json")
    master_dict = json.load(input_file)

    # start discord bot
    client = MyClient()
    client.run(open("token.txt", "r").read())
