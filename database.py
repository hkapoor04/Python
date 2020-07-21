import sqlite3

from cryptography.fernet import Fernet

conn = sqlite3.connect('application.db')

c = conn.cursor()

# Create table
#c.execute('CREATE TABLE account (username TEXT PRIMARY KEY, password TEXT, firstname TEXT, lastname TEXT, emailaddress TEXT)')

#c.execute('CREATE TABLE candidate (firstname TEXT , lastname TEXT, email TEXT, phonenumber INTEGER, currentlocation TEXT, workauthorization TEXT, resume BLOB, documents BLOB)')

#c.execute('select * from candidate')

#c.execute('SELECT * FROM CANDIDATE')

#for row in c.fetchall():
#    print(row)

#c.execute('CREATE TABLE security(key TEXT)')

#c.execute('SELECT * FROM candidate')

c.execute('ALTER TABLE candidate add column status TEXT')

#for row in c.fetchall():
#   print(row)

# c.execute('SELECT * FROM SECURITY')
#
# for row in c.fetchall():
#    print(row)

# password = 'Welcome'
#
# for row in c.fetchone():
#    str_key = str(row, 'utf-8')
#    print(str_key)
#    cipher_suite = Fernet(str.encode(str_key))
#    encrypted_password = cipher_suite.encrypt(str.encode(password))
#    print(encrypted_password)


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed else they will be lost.
conn.close()