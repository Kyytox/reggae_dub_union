"""
Programme for init database postgreSQL

Create Table:
    - users
    - shops
    - vinyls
    - songs
    - favoris
"""

from dotenv import load_dotenv

# Fonctions utils
import utils as db_utils

load_dotenv()


def create_tables(conn):
    """Create tables in the database"""
    # execute sql query in sql_init.sql (file)
    with conn.cursor() as cur:
        with open("database/sql_init.sql", "r") as f:
            cur.execute(f.read())

    conn.commit()


def init_db():
    """Init database, create tables, insert data"""
    conn = db_utils.connect_db_psycopg2()

    if conn is None:
        print("Error: Could not make connection to the Postgres database")
        return None

    create_tables(conn)

    conn.close()


if __name__ == "__main__":
    init_db()
