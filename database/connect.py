import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2

load_dotenv()


def connect_db_psycopg2():
    """Create a connection to the database with psycopg2"""
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


def connect_db_sqlalchemy():
    """Create a connection to the database with sqlalchemy"""
    try:
        return create_engine(
            f'postgresql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PWD")}@localhost:5432/{os.getenv("DATABASE")}'
        )
    except Exception as e:
        print(e)
        return None
