import pandas as pd
import httpx
from selectolax.parser import HTMLParser

import functions_framework


# def scrap_controltower(name_shop: str, url: str) -> pd.DataFrame:
@functions_framework.http
def scrap_controltower(request: dict) -> pd.DataFrame:
    """
    Scrap controltower

    Args:
        name_shop (str): name of shop
        url (str): url to scrap

    Returns:
        pd.DataFrame: dataframe with data scrapped
    """

    name_shop = "Control Tower"
    url = "https://controltower.fr/fr/"

    results = pd.DataFrame()

    # parse HTML
    html = HTMLParser(httpx.get(url).text)

    # retrieve all tags article with class=product-miniature
    lst_items = html.css("a.product_img_link")

    # retrieve infos of the 70 first elements
    for vinyl in lst_items[:5]:
        vinyl_link = vinyl.attributes.get("href")

        # parse HTML
        html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)

        # retrieve infos if tag option exists
        if html_page_vinyl.css_matches("option"):

            # get vinyl title
            vinyl_title = html_page_vinyl.css_first("h1").text()
            print(f"Scrapping {vinyl_title}")

            # retrieve Image
            vinyl_image = html_page_vinyl.css_first("img#bigpic").attributes.get("src")

            # retrieve format vinyl
            format_vinyl = (
                html_page_vinyl.css_first("option")
                .text()
                .replace(")", "")
                .replace("(", "")
                .replace('"', "")
            )

            # retrieve all mp3
            lst_mp3 = html_page_vinyl.css("source")

            for mp3 in lst_mp3:
                mp3_title = mp3.attributes.get("title")
                mp3_link = mp3.attributes.get("src")

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

    print(f"Scrapped {len(results)} items from {name_shop}")
    print(results)
    print(results.iloc[0])

    # to dict
    results = results.to_dict(orient="records")

    return results
