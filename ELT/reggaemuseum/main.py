import re
import pandas as pd
import httpx
from selectolax.parser import HTMLParser

import functions_framework


# def scrap_reggaemuseum(name_shop: str, url: str) -> pd.DataFrame:
@functions_framework.http
def scrap_reggaemuseum(request: dict) -> pd.DataFrame:
    """
    Scrap reggaemuseum

    Args:
        client (httpx.AsyncClient): client httpx
        name_shop (str): name of shop
        url (str): url to scrap

    Returns:
        pd.DataFrame: dataframe with data scrapped
    """

    name_shop = "reggaemuseum"
    list_urls = [
        "https://www.reggae-museum.com/shop/24-dancehall-new-roots#orderby=position&orderway=desc&n=40&p=",
        "https://www.reggae-museum.com/shop/26-rub-a-dub-early-digital#orderby=position&orderway=desc&n=40&p=",
        "https://www.reggae-museum.com/shop/27-ska-rocksteady-roots#orderby=position&orderway=desc&n=40&p=",
        "https://www.reggae-museum.com/shop/28-12-inch-records#orderby=position&orderway=desc&n=40&p=",
    ]

    results = pd.DataFrame()

    # random_page = 1

    # dict_pages = {
    #     "https://www.reggae-museum.com/shop/14": 22,
    #     "https://www.reggae-museum.com/shop/15": 42,
    #     "https://www.reggae-museum.com/shop/16": 13,
    #     "https://www.reggae-museum.com/shop/18": 2,
    # }

    # # get random page
    # base_url = url.split("-", 2)[0] + "-" + url.split("-", 2)[1]
    # end_url = url.split("-", 2)[2]
    # random_page = random.randint(1, dict_pages[base_url])
    # url = base_url + "-" + end_url + str(random_page)

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags article with class=album-block
        lst_articles = html.css("div.product-container")

        for vinyl in lst_articles[:3]:

            vinyl_image = vinyl.css_first("img.img-responsive").attributes.get("src")
            vinyl_link = vinyl.css_first("a.product_img_link").attributes.get("href")

            vinyl_title = re.sub(
                " +",
                " ",
                vinyl.css_first("a.product-name")
                .text()
                .replace("\n", " ")
                .replace("\t", " "),
            )

            #  open url link_vinyl for retrieve mp3 link
            html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)

            # Extract format from title
            if re.search(r"\b(7|10|12|lp|LP)\b", vinyl_title):
                format_vinyl = re.search(r"\b(7|10|12|lp|LP)\b", vinyl_title).group(1)
            else:
                format_vinyl = "12"

            div_content = html_page_vinyl.css_first("section.page-product-box")

            lst_infos = re.sub(
                " +", " ", div_content.text().replace("\n", " ").replace("\t", " ")
            ).split("] ")

            # get artitst if br.text contains "Artist")
            lst_articles = [
                item.split(": ")[1].split("[")[0].strip()
                for item in lst_infos
                if "Artist" in item
            ]

            # get Title if br.text contains "Title"
            lst_titles = [
                item.split(": ")[1].split("[")[0].strip()
                for item in lst_infos
                if "Title" in item
            ]

            # get audio
            lst_mp3 = div_content.css("audio")

            for i in range(len(lst_mp3)):
                mp3_title = lst_titles[i]
                mp3_link = lst_mp3[i].css_first("source").attributes.get("src")

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


scrap_reggaemuseum({})
