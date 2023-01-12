import sqlite3

connection = sqlite3.connect("Planner.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE user(nameUser string, nickUser string, birthUser string,"
               "emailUser string, passwordUser string)")

cursor.execute("CREATE TABLE events(title string, location string, userEmail string)")


connection.close()
