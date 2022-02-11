import math
import random
import time

import mysql.connector


def create_user(db, user_id):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT * FROM student WHERE discord_id=%s', [f"{user_id}"])
        record = cursor.fetchall()
        if record:
            return

        print(user_id, "not located, creating record now.")
        cursor.execute(
            'INSERT INTO student(discord_id, total_msg, last_msg, counted_msg, multiplier, total_xp) VALUES(%s, 1, 0, 1, 1, 0)',
            [f"{user_id}"])
        db.commit()

    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


async def increase_xp(db, message, bot):
    if message.author.bot:
        return
    user_id = message.author.id
    msg_time_unix = time.mktime(message.created_at.timetuple())
    create_user(db, user_id)
    cursor = db.cursor()
    previous_last_msg = get_last_message(db, user_id)
    prior_level = get_level(get_xp(db, user_id))
    try:  # Set last_msg equal to the time of the last message sent per-user
        cursor.execute('UPDATE student SET last_msg=%s,total_msg=total_msg+1 WHERE discord_id=%s',
                       [f"{msg_time_unix}", f"{user_id}"])
        db.commit()
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    new_last_msg = get_last_message(db, user_id)
    cooldown = new_last_msg - previous_last_msg
    multiplier = get_multiplier(db, user_id)
    if cooldown > 30:
        xp = random.randint(2, 8) * multiplier
        cursor.execute('UPDATE student SET counted_msg=counted_msg+1,total_xp=total_xp+%s WHERE discord_id=%s',
                       [f"{xp}", f"{user_id}"])
        db.commit()
    cursor.close()
    new_level = get_level(get_xp(db, user_id))
    if new_level>prior_level:
        bot_spam = bot.get_channel(931418786517647360)
        await bot_spam.send(message.author + " has ranked up to level " + new_level + "!")


def update_msg_time(db, message):
    create_user(db, message.author.id)
    msg_time_unix = time.mktime(message.created_at.timetuple())
    cursor = db.cursor()
    try:
        cursor.execute('UPDATE student SET last_msg=%s WHERE discord_id=%s',
                       [f"{msg_time_unix}", f"{message.author.id}"])
        db.commit()
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def fetch_user(db, user_id):
    create_user(db, user_id)
    cursor = db.cursor()
    try:
        cursor.execute('SELECT * FROM student WHERE discord_id=%s', [f"{user_id}"])
        record = cursor.fetchone()
        return record
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def get_last_message(db, user_id):
    create_user(db, user_id)
    cursor = db.cursor()
    try:
        cursor.execute('SELECT last_msg FROM student WHERE discord_id=%s', [f"{user_id}"])
        record = cursor.fetchone()
        return record[0]
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def get_xp(db, user_id):
    create_user(db, user_id)
    cursor = db.cursor()
    try:
        cursor.execute('SELECT total_xp FROM student WHERE discord_id=%s', [f"{user_id}"])
        record = cursor.fetchone()
        return record[0]
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()

def get_level(xp):
    return math.floor(-2.5 + math.sqrt(8 * xp + 1225) / 10)

def get_rank(db, user_id):
    create_user(db, user_id)
    cursor = db.cursor()
    try:
        cursor.execute('SELECT * FROM student ORDER BY total_xp DESC')
        records = cursor.fetchall()
        rank = 0
        for record in records:
            rank += 1
            if int(record[0]) == user_id:
                break

        return rank
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def get_multiplier(db, user_id):
    create_user(db, user_id)
    cursor = db.cursor()
    try:
        cursor.execute('SELECT multiplier FROM student WHERE discord_id=%s', [f"{user_id}"])
        record = cursor.fetchone()
        return float(record[0])
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def update_multiplier(db, user_id, amount):
    create_user(db, user_id)
    cursor = db.cursor()
    try:
        cursor.execute('UPDATE student SET multiplier=%s WHERE discord_id=%s',
                       [f"{amount}", f"{user_id}"])
        db.commit()
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def top_ten(db):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT discord_id FROM student ORDER BY total_xp DESC LIMIT 10')
        record = cursor.fetchall()
        return record
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def get_courses(db, to_search):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT * FROM course WHERE subj=%s', [f"{to_search}"])
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def get_section(db, subj, code):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT * FROM section AS section JOIN course AS course JOIN taught_by as taught_by WHERE section.subj=%s AND '
                       'section.num=%s AND section.num=course.num AND section.subj=course.subj AND taught_by.crn=section.crn ORDER BY section.sec_num ASC', [f"{subj}", f"{code}"])
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def get_professors(db, to_search):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT name, title, email, phone, office, picture FROM instructor WHERE name LIKE %s',
                       [f"%{to_search}%"])
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()


def get_professor_sections(db, professor):
    cursor = db.cursor()
    try:
        cursor.execute('SELECT subj, num, sec_num, days, time FROM taught_by AS teaches JOIN section AS sec WHERE '
                       'instructor LIKE %s AND teaches.crn=sec.crn', [f"%{professor}%"])
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as exc:
        print("Something went wrong: {}".format(exc))
    cursor.close()
