"""
Programme for init database postgreSQL

Create Table:
    - users
    - shops
    - vinyls
    - songs
    - favoris
"""


import os
from dotenv import load_dotenv
import psycopg2

import sql_query as sql

load_dotenv()


def init_conn():
    """Create a connection to the database"""
    try:
        return psycopg2.connect(
            host="localhost",
            port=5432,
            database=os.getenv("DATABASE"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PWD"),
        )

    except psycopg2.Error as e:
        print(e)
        return None


def create_tables(conn):
    """Create tables in the database"""
    with conn.cursor() as cur:
        cur.execute(sql.create_shops)
        cur.execute(sql.create_vinyls)
        cur.execute(sql.create_songs)
        cur.execute(sql.create_users)
        cur.execute(sql.create_favoris)

    conn.commit()


def main():
    conn = init_conn()

    if conn is None:
        print("Error: Could not make connection to the Postgres database")
        return None

    create_tables(conn)

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
