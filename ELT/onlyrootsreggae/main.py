import html
import pandas as pd
import httpx
from selectolax.parser import HTMLParser

import functions_framework


# def scrap_onlyrootsreggae(name_shop: str, url: str) -> pd.DataFrame:
@functions_framework.http
def scrap_onlyrootsreggae(request: dict) -> pd.DataFrame:
    """
    Scrap onlyrootsreggae

    Args:
        client (httpx.AsyncClient): client httpx
        name_shop (str): name of shop
        url (str): url to scrap

    Returns:
        pd.DataFrame: dataframe with data scrapped
    """

    name_shop = "onlyrootsreggae"
    list_urls = [
        "https://www.onlyroots-reggae.com/fr/21-singles-7-45t/s-1/?page=1&order=product.date_add.desc",
        "https://www.onlyroots-reggae.com/fr/20-maxis-12-10/s-1/?page=1&order=product.date_add.desc",
        "https://www.onlyroots-reggae.com/fr/17-albums-lp-33t/s-1/?page=1&order=product.date_add.desc",
    ]

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags article with class=product-miniature
        lst_articles = html.css("article.product-miniature")

        for vinyl in lst_articles[:3]:
            vinyl_link = vinyl.css_first("link").attributes.get("href")

            # parse HTML
            html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)

            if html_page_vinyl.css_matches("source"):
                vinyl_title = html_page_vinyl.css_first("h1.page-heading").text()
                vinyl_image = html_page_vinyl.css_first("img.img-fluid").attributes.get(
                    "src"
                )
                format_vinyl = (
                    vinyl_title.split(" ")[0]
                    .replace(")", "")
                    .replace("(", "")
                    .replace('"', "")
                )

                # retrieve all mp3
                lst_mp3 = html_page_vinyl.css("source")

                for mp3 in lst_mp3:
                    mp3_title = mp3.attributes.get("title")
                    mp3_link = "https://www.onlyroots-reggae.com" + mp3.attributes.get(
                        "src"
                    )

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


scrap_onlyrootsreggae({})
