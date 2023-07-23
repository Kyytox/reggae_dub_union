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

load_dotenv()


def init_conn():
    """Create a connection to the database"""
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database=os.getenv("DATABASE"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PWD"),
    )


def main():
    conn = init_conn()

    if conn.closed:
        print("The connection is closed.")

    # Close the connection
    conn.close()


if __name__ == "__main__":
    main()
