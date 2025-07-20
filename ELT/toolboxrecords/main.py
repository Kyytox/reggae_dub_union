import pandas as pd
import httpx
from selectolax.parser import HTMLParser

import functions_framework


# def scrap_toolboxrecords(name_shop: str, url: str) -> pd.DataFrame:
@functions_framework.http
def scrap_toolboxrecords(request: dict) -> pd.DataFrame:
    """
    Scrap toolboxrecords

    Args:
        client (httpx.AsyncClient): client httpx
        name_shop (str): name of shop
        url (str): url to scrap

    Returns:
        pd.DataFrame: dataframe with data scrapped
    """

    name_shop = "toolboxrecords"
    list_urls = [
        "https://www.toolboxrecords.com/fr/catalog/list/categoryID/3/item_nbr/60",
    ]

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags article with class=product-miniature
        lst_articles = html.css("div.product-cell-thumb")

        for vinyl in lst_articles[:4]:
            if vinyl.css_matches("ul.product-track-listing"):
                vinyl_image = vinyl.css_first("img").attributes.get("src")
                vinyl_link = vinyl.css_first("a").attributes.get("href")
                vinyl_title = (
                    vinyl.css_first("span.product-name").text()
                    + " - "
                    + vinyl.css_first("div.product-infos-details")
                    .css_first("li")
                    .text()
                )

                # Format vinyl
                format_vinyl = (
                    vinyl.css_first("div.product-infos-details").css_first("ul").text()
                )
                if '7"' in format_vinyl or "7''" in format_vinyl:
                    format_vinyl = "7"
                elif "LP" in format_vinyl or "CD" in format_vinyl:
                    format_vinyl = "LP"
                elif "10''" in format_vinyl:
                    format_vinyl = "10"
                else:
                    format_vinyl = "12"

                if vinyl.css_matches("li.more-tracks-link"):
                    # open url link_vinyl for retrieve mp3 link because all mp3 is not is main page
                    # parse HTML
                    html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)
                    div_mp3 = html_page_vinyl.css_first("ul.product-track-listing")
                else:
                    div_mp3 = vinyl.css_first("ul.product-track-listing")

                lst_mp3 = div_mp3.css("li")

                for mp3 in lst_mp3[:-1]:
                    mp3_title = mp3.css_first("div.track-title").text()
                    mp3_link = (
                        "https://www.toolboxrecords.com/public/mp3/"
                        + mp3.css_first("div.track-title").attributes.get("rel")
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


scrap_toolboxrecords({})
