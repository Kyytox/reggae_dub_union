import pandas as pd
import sys
import httpx
import asyncio
import nest_asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Fonctions utils
from database import utils as db_utils
import scripts_scrap as sc

nest_asyncio.apply()


def get_shop_links(conn: str) -> pd.DataFrame:
    """Get shop list from DB"""
    return pd.read_sql("SELECT * FROM shops", conn)


async def scrap_shop(name_function: str, name_shop: str, links: list, conn: str) -> None:
    """Scrap shop"""
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        func = getattr(sc, name_function)
        tasks.extend(func(client, name_shop, link) for link in links)
        df = await asyncio.gather(*tasks)

    df = pd.concat(df, ignore_index=True)

    if not df.empty:
        insert_in_db(df, conn)


def insert_in_db(df: pd.DataFrame, conn: str) -> None:
    """Insert data in DB in extract_vinyls_temp"""

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
    """Collect shops to scrap
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
        # print(name_function)
        # print(links)

        # scrap shop
        asyncio.run(scrap_shop(name_function, name_shop, links, conn))

        print("---------------------")

    conn.dispose()


if __name__ == "__main__":
    extract_data()
