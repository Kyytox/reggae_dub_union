"""
file: extract_data.py

Extract data from shops

- Collect shops to scrap
- Browse shops
- Scrap shop
- Insert data in DB

"""

import pandas as pd
import httpx
import asyncio
import nest_asyncio

# Fonctions utils
from helpers import connect as db_utils
from operators import scripts_scrap as sc

nest_asyncio.apply()


def get_shop_links(conn: str) -> pd.DataFrame:
    """
    Get all shops in DB

    Args:
        conn (str): connection to db

    Returns:
        pd.DataFrame: dataframe with elements of Table shops (name, name_function, links)
    """
    return pd.read_sql("SELECT * FROM shops", conn)


async def scrap_shop(name_function: str, name_shop: str, links: list, conn: str) -> None:
    """
    Scrap shops links in parallel using asyncio.

    Args:
        name_function (str): name of function to scrap shop
        name_shop (str): name of shop
        links (list): list of links to scrap
        conn (str): connection to db
    """
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        func = getattr(sc, name_function)
        tasks.extend(func(client, name_shop, link) for link in links)
        df = await asyncio.gather(*tasks)

    df = pd.concat(df, ignore_index=True)

    if not df.empty:
        insert_in_db(df, conn)


def insert_in_db(df: pd.DataFrame, conn: str) -> None:
    """
    Insert data in DB in extract_vinyls_temp

    Args:
        df (pd.DataFrame): dataframe with data to insert
        conn (str): connection to db
    """
    # kepp vinyl_link, start with "http"
    df = df[df["vinyl_link"].str.startswith("http")]

    df = df.rename(
        columns={
            "name_shop": "site",
            "format_vinyl": "format",
            "vinyl_title": "title",
            "vinyl_image": "image",
            "vinyl_link": "url",
            "mp3_title": "title_mp3",
            "mp3_link": "mp3",
        }
    )

    # Insert data
    df.to_sql("extract_vinyls_temp", conn, if_exists="append", index=False)


def extract_data():
    """
    Collect shops to scrap
    Browse shops
    Scrap shop
    Insert data in DB
    """
    # connect to db with sqlalchemy for use pandas to_sql
    conn = db_utils.connect_db_sqlalchemy()

    df_list_shops = get_shop_links(conn)

    # browse shops
    for index, row in df_list_shops.iterrows():
        name_shop = row["name"]
        name_function = row["name_function"]
        links = row["links"]

        print(name_shop)

        # scrap shop
        asyncio.run(scrap_shop(name_function, name_shop, links, conn))

    conn.dispose()
