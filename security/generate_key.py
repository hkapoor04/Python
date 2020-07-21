from cryptography.fernet import Fernet
import sqlite3

key = Fernet.generate_key()
conn = sqlite3.connect('../database/application.db')
c = conn.cursor()

c.execute('INSERT INTO security VALUES(?)', (key,))

conn.commit()
conn.close()
