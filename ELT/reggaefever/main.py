import pandas as pd
import httpx
from selectolax.parser import HTMLParser

import functions_framework


# def scrap_reggaefever(name_shop: str, url: str) -> pd.DataFrame:
@functions_framework.http
def scrap_reggaefever(request: dict) -> pd.DataFrame:
    """
    Scrap reggaefever

    Args:
        client (httpx.AsyncClient): client httpx
        name_shop (str): name of shop
        url (str): url to scrap

    Returns:
        pd.DataFrame: dataframe with data scrapped
    """

    name_shop = "reggaefever"
    list_urls = [
        "https://www.reggaefever.ch/catalog?format=7&sort=relDate_riddim",
        "https://www.reggaefever.ch/articleList?format=10&newRel=0&sort=relDate_riddim",
        "https://www.reggaefever.ch/articleList?format=12&newRel=0&sort=relDate_riddim&noStyle=Hip+Hop&noStyle=R%2BB",
    ]

    results = pd.DataFrame()

    date_ann = [str(i) for i in range(2000, 2050)]

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags tr
        lst_articles = html.css("tr")

        for item in lst_articles[1:9]:
            if item.text().lstrip()[:4] not in date_ann:
                if item.css_matches("td.articleFormat"):
                    format_vinyl = item.css_first("td.articleFormat").text()

                if item.css_matches("td.artist"):
                    if item.css_first("td.artist").text() != "":
                        vinyl_title = (
                            item.css_first("td.artist").text()
                            + " - "
                            + item.css_first("td.title").text()
                        )
                        save_title = vinyl_title
                    else:
                        vinyl_title = save_title

                if item.css_matches("img.articleIcon"):
                    vinyl_image = item.css_first("img.articleIcon").attributes.get(
                        "src"
                    )

                if item.css_matches("a"):
                    if "articleId" in item.css_first("a").attributes.get("href"):
                        vinyl_link = "https://www.reggaefever.ch/" + item.css_first(
                            "a"
                        ).attributes.get("href")
                        save_link = vinyl_link
                    else:
                        vinyl_link = save_link

                if item.css_matches("td.title"):
                    mp3_title = item.css_first("td.title").text()
                else:
                    mp3_title = "version"

                if item.css_matches("a[target=rfplayer]"):
                    mp3_link = item.css_first("a[target=rfplayer]").attributes.get(
                        "href"
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


scrap_reggaefever({})
