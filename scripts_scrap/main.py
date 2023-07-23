import pandas as pd
import os
import csv
import time
import random
import httpx
import asyncio
import nest_asyncio
from urllib.request import urlretrieve


import scripts_scrap as sc

nest_asyncio.apply()


TEMP_DIR = "scripts_scrap/temp"


shops = [
    "jahwaggysrecords",
    "onlyrootsreggae",
    "controltower",
    "reggaefever",
    "pataterecords",
    "toolboxrecords",
    "lionvibes",
    "reggaemuseum",
]


def get_shop_links(name_shop: str) -> tuple:
    # read cdv shops.csv
    df = pd.read_csv("shops.csv", sep=";", header=0)

    # links
    links = df[df["name_shop"] == name_shop]["links"].to_list()[0].split(",")
    name_function = df[df["name_shop"] == name_shop]["name_function"].values[0]

    return links, name_function


async def scrap_shop(name_function: str, name_shop: str, links: list) -> None:
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        func = getattr(sc, name_function)
        tasks.extend(func(client, name_shop, link) for link in links)
        df = await asyncio.gather(*tasks)

    df = pd.concat(df, ignore_index=True)
    print(df)

    if not df.empty:
        df.to_parquet(f"{TEMP_DIR}/{name_shop}_temp.parquet", engine="pyarrow", compression="snappy")


def main():
    for name_shop in shops:
        links, name_function = get_shop_links(name_shop)

        print(name_shop)
        print(links)
        print(name_function)

        asyncio.run(scrap_shop(name_function, name_shop, links))

        print("---------------------")


if __name__ == "__main__":
    main()
