"""
Programme for transform data 
Transfer data from extract_vinyls_temp to vinyls, songs
"""

import sys
from dotenv import load_dotenv
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Fonctions utils
import database.utils as db_utils
import database.sql_query as sql


load_dotenv()


def transform_tables():
    """Transform data from extract_vinyls_temp to vinyls, songs"""

    # connect to database
    conn = db_utils.connect_db_sqlalchemy()

    # insert data in vinyls
    with conn.connect() as cur:
        cur.execute(sql.insert_vinyls)
        cur.execute(sql.insert_songs)
        cur.execute(sql.truncate_extract_vinyls_temp)

    conn.dispose()
