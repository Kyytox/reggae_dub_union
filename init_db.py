import sqlite3

connection = sqlite3.connect('bd_vinyls_dub_scrap.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (name, password) VALUES (?, ?)",
            ('kytox', 'test')
            )

cur.execute("CREATE TABLE favoris (name_user TEXT, title_vinyl TEXT, image_vinyl TEXT, url_vinyl TEXT, title_mp3 TEXT, file_mp3 TEXT, duration_mp3 TEXT)")


connection.commit()
connection.close()