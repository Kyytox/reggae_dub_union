import pandas as pd
import httpx
from selectolax.parser import HTMLParser

import functions_framework


# def scrap_jahwaggysrecords(name_shop: str, url: str) -> pd.DataFrame:
@functions_framework.http
def scrap_jahwaggysrecords(request: dict) -> pd.DataFrame:
    """
    Scrap jahwaggysrecords

    Args:
        client (httpx.AsyncClient): client httpx
        name_shop (str): name of shop
        url (str): url to scrap

    Returns:
        pd.DataFrame: dataframe with data scrapped
    """

    name_shop = "jahwaggysrecords"
    list_urls = [
        "https://jahwaggysrecords.com/fr/5-brand-new-7-vinyl-selection",
        "https://jahwaggysrecords.com/fr/6-brand-new-10-vinyl-selection",
        "https://jahwaggysrecords.com/fr/7-brand-new-12-vinyl-selection",
        "https://jahwaggysrecords.com/fr/8-brand-new-lp-vinyl-selection",
        "https://jahwaggysrecords.com/fr/18-test-press-selection",
    ]

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # get format vinyl
        format_vinyl = url[44:46].replace("-", "")
        format_vinyl = "test press" if format_vinyl == "s" else format_vinyl

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags article with class=product-miniature
        lst_articles = html.css("article.product-miniature")

        for vinyl in lst_articles[:2]:
            vinyl_title = vinyl.css_first("h3.product-title").text()
            vinyl_image = vinyl.css_first("img").attributes.get("src")
            vinyl_link = vinyl.css_first("a").attributes.get("href")

            print(f"Scrapping {vinyl_title}")

            # parse HTML
            html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)

            # Find list Audio
            lst_audio = html_page_vinyl.css_first("div#mp3player")

            # Get mp3 Titles
            lst_titles = lst_audio.css("h3")

            # Get mp3 Links
            lst_mp3 = lst_audio.css(".audioPlayer")

            # mp3 infos
            for i in range(len(lst_mp3)):
                mp3_title = lst_titles[i].text()
                mp3_link = "https://jahwaggysrecords.com" + lst_mp3[i].attributes.get(
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


scrap_jahwaggysrecords({})
