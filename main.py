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
            # embed_builder = discord.Embed(color=0x184b91)
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
        # some argument was given
        # argument can be course and optionally the section
        if len(split) > 2:
            return "length is 2 or more (an course argument was given)"
        # just info

        # check if channel is in comp
        name = message.channel.name.lower()
        if "comp" not in name:
            embed_builder.title = "Invalid channel"
        else:
            embed_builder.title = name.upper()  # + " Info"
            # check for valid class shouldn't be needed because classes are added manually
            # you can only do this because we know the format is COMP-XXXX
            temp = name.split('-')
            name = temp[0].upper() + temp[1]

            temp_dict = master_dict["Courses"][name]
            embed_builder.description = temp_dict["name"]

            embed_builder.add_field(name="Hours", value=temp_dict["hours"], inline=False)
            # todo:
            '''
            make this its own function so that you don't have to write it a 
            second time for when people request a specific section
            '''
            if "sections" in temp_dict:
                for section in temp_dict["sections"]:
                    embed_builder.add_field(
                        name=section,
                        value=json.dumps(temp_dict["sections"][section]).replace(',', "\n"),
                        inline=False
                        )

    elif leading == "professors":
        # header and description
        embed_builder.title = "Computer Science Professors"
        embed_builder.description = "A list of all Full-Time Faculty in the Computer Science Department"

        # adding all the individual professors
        for professor in master_dict["Professors"]:
            embed_builder.add_field(name=professor, value=master_dict["Professors"][professor]["title"], inline=True)

    elif leading == "professor":
        # grabs everything after "professor "
        professor_name = message.content.split("professor ")[1].lower()
        # find professor that has at least part of one of the professor keys
        for professor in master_dict["Professors"]:
            if professor_name in professor.lower():
                # set title to professor
                embed_builder.title = str(professor).title()
                # adding email, title, office fields
                embed_builder.add_field(name="Email", value=master_dict["Professors"][professor]["email"], inline=False)
                embed_builder.add_field(name="Title", value=master_dict["Professors"][professor]["title"], inline=False)
                embed_builder.add_field(name="Office", value=master_dict["Professors"][professor]["office"], inline=False)
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


def fix_class_name(name):
    new_name = ""
    temp = name.split('-')
    new_name += temp[0] + temp[1]
    if len(temp) > 2:
        new_name += '-' + temp[2]
    return new_name


def strip_email(email):
    username = email.split("@")[0];
    return username.replace(".", "")
    return username


def get_class(class_name):
    return "something"


if __name__ == "__main__":
    # import info
    input_file = open("updated.json")
    master_dict = json.load(input_file)

    # start discord bot
    client = MyClient()
    client.run(open("token.txt", "r").read())
