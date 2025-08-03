import sqlite3

conn = sqlite3.connect('users.db')
cursor=conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               email TEXT UNIQUE,
               code TEXT
               )
                ''')
conn.commit()
conn.close()
print("Database and users table created")