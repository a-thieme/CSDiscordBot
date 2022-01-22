import mysql.connector


def get_connection():
    print("Establishing connection to University database")
    return mysql.connector.connect(host='localhost', port=3306, user='root', password='',
                                   database="university")
