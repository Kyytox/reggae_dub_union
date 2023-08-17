"""file : test_db.py

Test if connection to database is working
"""

from dotenv import load_dotenv

from helpers.connect import connect_db_psycopg2, connect_db_sqlalchemy

load_dotenv()


def test_connection():
    """Test if connection to database is working

    Assert:
        conn (str): connection to db
    """
    conn = connect_db_psycopg2()
    assert conn is not None, "Connection to database with psycopg2 failed"

    conn = connect_db_sqlalchemy()
    assert conn is not None, "Connection to database with sqlalchemy failed"
