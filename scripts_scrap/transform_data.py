"""
Programme for transform data 
Transfer data from extract_vinyls_temp to vinyls, songs
"""

import sys
from dotenv import load_dotenv
from pathlib import Path
import sqlalchemy

# sys.path.append(str(Path(__file__).resolve().parent.parent))

# Fonctions utils
from database import connect as db_utils
from database import sql_queries as sql

load_dotenv()


def transform_tables():
    """
    Transform data from extract_vinyls_temp to vinyls, songs

    - connect to database
    - insert data of extract_vinyls_temp in vinyls
    - insert data of extract_vinyls_temp in songs
    - truncate extract_vinyls_temp

    """
    # connect to database
    conn = db_utils.connect_db_sqlalchemy()

    # insert data in vinyls
    with conn.connect() as cur:
        cur.execute(sqlalchemy.text(sql.insert_vinyls))
        cur.execute(sqlalchemy.text(sql.insert_songs))
        cur.execute(sqlalchemy.text(sql.truncate_extract_vinyls_temp))
        cur.commit()

    conn.dispose()
