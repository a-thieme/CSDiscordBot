import math
import re

from discord import File
from easy_pil import Canvas, Editor, Font, load_image
from table2ascii import table2ascii as t2a, PresetStyle

from Core.Database.Queries import get_rank, get_xp, top_ten


def get_rank_card(event, user):
    user_data = get_user_data(event, user)

    background = Editor(Canvas((900, 300), color="#00488f"))

    # For profile to use users profile picture load it from url using the load_image/load_image_async function
    profile_image = load_image(str(user.avatar_url))
    profile = Editor(profile_image).resize((150, 150)).circle_image()

    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)

    card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

    background.polygon(card_right_shape, "#40b4e5")
    background.paste(profile, (30, 30))

    background.rectangle((30, 220), width=650, height=40, fill="#494b4f", radius=20)
    background.bar(
        (30, 220),
        max_width=650,
        height=40,
        percentage=user_data["percentage"],
        fill="#8c9292",
        radius=20,
    )
    background.text((200, 40), user_data["name"], font=poppins, color="white")

    background.text((200, 175), f"Rank : {user_data['rank']}", font=poppins_small, color="white")

    background.rectangle((200, 100), width=350, height=2, fill="#ffffff")
    background.text(
        (200, 130),
        f"Level : {user_data['level']} "
        + f" XP : {user_data['xp']} / {user_data['next_level_xp']}",
        font=poppins_small,
        color="white",
    )

    file = File(fp=background.image_bytes, filename="rank_card.png")
    return file


async def get_leaderboard_card(event):
    lb = top_ten(event.get_database())
    table = []
    for user in lb:
        user = await event.get_user_by_id(user[0])
        user_data = get_user_data(event, user)
        table.append(list(user_data.values()))
    for col in table:
        del col[2], col[2], col[3]
        col[1] = re.sub(r'[^A-z0-9!@#$%^&*()-_\s]+', '', col[1]) # [A-z]{2,4}[0-9]{3,4}
    output = t2a(header=['Rank', 'User', 'Level'], body=table, style=PresetStyle.thin_compact_rounded, last_col_heading=True)
    return f"```css\n{output}\n```"


def get_level(xp):
    return math.floor(-2.5 + math.sqrt(8 * xp + 1225) / 10)


def get_xp_for_level(level):
    return int((((25 * math.pow(level, 2)) + 125 * level) / 2) - 75)


def get_user_data(event, user):
    xp = get_xp(event.get_database(), user.id)
    xp_for_next = get_xp_for_level(get_level(xp) + 1)
    return {
        "rank": "#" + str(get_rank(event.get_database(), user.id)),
        "name": user.display_name,
        "xp": xp - get_xp_for_level(get_level(xp)),
        "next_level_xp": xp_for_next - get_xp_for_level(get_level(xp)),
        "level": get_level(xp),
        "percentage": (xp - get_xp_for_level(get_level(xp))) / (xp_for_next - get_xp_for_level(get_level(xp))) * 100,
    }
