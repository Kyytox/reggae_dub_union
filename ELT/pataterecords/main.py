import pandas as pd
import httpx
from selectolax.parser import HTMLParser

import functions_framework


# def scrap_pataterecords(name_shop: str, url: str) -> pd.DataFrame:
@functions_framework.http
def scrap_pataterecords(request: dict) -> pd.DataFrame:
    """
    Scrap pataterecords

    Args:
        client (httpx.AsyncClient): client httpx
        name_shop (str): name of shop
        url (str): url to scrap

    Returns:
        pd.DataFrame: dataframe with data scrapped
    """

    name_shop = "pataterecords"
    list_urls = [
        "https://www.patate-records.com/shop/1/1/1/type/1/",
        "https://www.patate-records.com/shop/1/1/1/type/2/",
        "https://www.patate-records.com/shop/1/1/1/type/3/",
    ]

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags article with class=product-miniature
        lst_articles = html.css("div.img_shop_article")

        for vinyl in lst_articles[:3]:
            vinyl_image = vinyl.css_first("img").attributes.get("src")
            vinyl_link = vinyl.css_first("a").attributes.get("href")

            # parse HTML
            html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)

            # if mp3 exist => retreive elements
            if html_page_vinyl.css_matches("audio"):
                vinyl_title = html_page_vinyl.css_first("h1").text()

                # list mp3
                div_mp3 = html_page_vinyl.css_first("div#traclist")
                lst_mp3 = div_mp3.css("div")

                # Format vinyl
                div_format = html_page_vinyl.css_first("div#caracteristic")
                format_vinyl = div_format.css_first("span").text()

                if "7" in format_vinyl:
                    format_vinyl = "7"
                elif "LP" in format_vinyl:
                    format_vinyl = "lp"
                elif len(lst_mp3) < 5:
                    format_vinyl = "10"
                else:
                    format_vinyl = "12"

                for mp3 in lst_mp3[:-1]:
                    if mp3.css_matches("source"):
                        mp3_title = mp3.text().split("\n")[-1]
                        mp3_link = mp3.css_first("source").attributes.get("src")

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


scrap_pataterecords({})
