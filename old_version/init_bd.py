import sqlite3

connection = sqlite3.connect('vinyls_dub_scrap.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()


