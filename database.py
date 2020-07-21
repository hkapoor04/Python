import sqlite3

conn = sqlite3.connect('application.db')

c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS account (username TEXT PRIMARY KEY, password TEXT, firstname TEXT, lastname TEXT, emailaddress TEXT)')

c.execute('CREATE TABLE IF NOT EXISTS candidate (firstname TEXT , lastname TEXT, email TEXT, phonenumber INTEGER, currentlocation TEXT, workauthorization TEXT, resume BLOB, documents BLOB)')

c.execute('ALTER TABLE candidate add column status TEXT')

conn.commit()

conn.close()