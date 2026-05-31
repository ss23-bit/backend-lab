import sqlite3

conn = sqlite3.connect("database-1.db", check_same_thread=False)

cursor = conn.cursor()

