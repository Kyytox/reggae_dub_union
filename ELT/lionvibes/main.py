import pandas as pd
import httpx
from selectolax.parser import HTMLParser

import functions_framework


# def scrap_lionvibes(name_shop: str, url: str) -> pd.DataFrame:
@functions_framework.http
def scrap_lionvibes(request: dict) -> pd.DataFrame:
    """
    Scrap lionvibes

    Args:
        client (httpx.AsyncClient): client httpx
        name_shop (str): name of shop
        url (str): url to scrap

    Returns:
        pd.DataFrame: dataframe with data scrapped
    """

    name_shop = "lionvibes"
    list_urls = [
        "https://www.lionvibes.com/collections/new-records?filter.p.m.custom.format=7%22&sort_by=created-descending",
        "https://www.lionvibes.com/collections/new-records?filter.p.m.custom.format=10%22&sort_by=created-descending",
        "https://www.lionvibes.com/collections/new-records?filter.p.m.custom.format=12%22&sort_by=created-descending",
        "https://www.lionvibes.com/collections/new-records?filter.p.m.custom.format=LP&sort_by=created-descending",
    ]

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)
        print(f"Parsed HTML from {html}")

        # retrieve all tags article with class=album-block
        # lst_articles = html.css("div.album-block")
        lst_articles = html.css("div.card--card")

        for vinyl in lst_articles[:3]:

            # Image
            vinyl_image = "https:" + vinyl.css_first("img").attributes.get("src")

            # Link + Title
            div_link = vinyl.css("a")
            vinyl_link = "https:" + div_link[1].attributes.get("href")

            # infos
            lst_infos = vinyl.css_first("div.card__metafields").css("p")

            # Artist and Title update
            artist_name = lst_infos[0].css_first("a").text().rstrip()
            vinyl_title = (
                (f"{div_link[1].text().rstrip()} - {artist_name}")
                .replace("\n", " ")
                .strip()
            )

            format_vinyl = (
                lst_infos[1]
                .text()
                .replace("Format: ", "")
                .replace("Double ", "")
                .replace('"', "")
            )

            # if vinyl.css_matches("div.col-xs-6"):
            lst_audio = vinyl.css_first("div.card__audio").css(".clip")
            print(f"Found {len(lst_audio)} audio clips for {vinyl_title}")

            # range title of track and collect filname attribute for mp3 link
            for track in lst_audio:
                mp3_title = track.css_first("strong").text()
                mp3_link = "https://shop.lionvibes.com" + track.css_first(
                    "source"
                ).attributes.get("src")

                row = {
                    "name_shop": name_shop,
                    "format_vinyl": format_vinyl,
                    "vinyl_title": vinyl_title,
                    "vinyl_image": vinyl_image,
                    "vinyl_link": vinyl_link,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                    "date_extract": pd.Timestamp.now(),
                }

                results = pd.concat(
                    [results, pd.DataFrame(row, index=[0])], ignore_index=True
                )

        print(f"Scrapped {len(results)} items")

    print(f"Scrapped {len(results)} items from {name_shop}")
    print(results)

    # to dict
    results = results.to_dict(orient="records")

    return results


scrap_lionvibes({})
