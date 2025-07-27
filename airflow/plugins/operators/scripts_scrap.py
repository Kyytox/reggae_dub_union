"""
regroup all functions to scrap vinyls
Each function scrap one shop

"""

import re
import pandas as pd
import random
import httpx
from selectolax.parser import HTMLParser


from airflow.models import Variable

from helpers.db_connect import (
    db_connect_postgres,
    get_specific_shop_links,
)

from helpers.utils_gcp_storage import upload_blob


def control_list_shops(name_shop: str, df_list_shops: pd.DataFrame) -> None:
    """
    Control if shop is in list of shops

    Args:
        name_shop (str): name of shop
        df_list_shops (pd.DataFrame): dataframe with list of shops
    """
    if df_list_shops.empty:
        raise ValueError(
            "No shops found in the database. Please check if table has data."
        )

    if name_shop not in df_list_shops["name_shop"].values:
        raise ValueError(
            f"Shop '{name_shop}' not found in the database. Please check the shop name."
        )


def save_file(
    df: pd.DataFrame, name_shop: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Save DataFrame to GCP Storage

    Args:
        df (pd.DataFrame): DataFrame to save
        name_shop (str): name of shop
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming
    """
    path_file = f"extract_{time_file_name}/{name_shop}.csv"
    upload_blob(bucket_name=bucket_name, df=df, destination_blob_name=path_file)


def scrap_jahwaggysrecords(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Scrap jahwaggysrecords

    Args:
        name_shop (str): name of shop
        conn_id (str): connection ID for the database
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming

    """
    print(f"Scrapping {name_shop}...")

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    # Get shop infos from DB
    df_list_shops = get_specific_shop_links(conn, name_shop)

    # Control if shop is in list of shops
    control_list_shops(name_shop, df_list_shops)

    list_urls = df_list_shops[df_list_shops["name_shop"] == name_shop]["links"].values

    print(f"Scrapping {name_shop} from URLs: {list_urls}")
    conn.close()

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

        for vinyl in lst_articles[2:4]:
            vinyl_title = vinyl.css_first("h3.product-title").text()
            vinyl_image = vinyl.css_first("img").attributes.get("src")
            vinyl_link = vinyl.css_first("a").attributes.get("href")
            vinyl_price = vinyl.css_first("span.price").text()

            print(f"Scrapping {vinyl_title}")

            # parse HTML
            html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)

            div_tabs = html_page_vinyl.css_first("div.tabs")

            if div_tabs.css_matches("div.product-reference"):
                vinyl_ref = (
                    div_tabs.css_first("div.product-reference").css_first("span").text()
                )
            else:
                vinyl_ref = vinyl_title

            # Find list Audio
            lst_audio = html_page_vinyl.css_first("div#mp3player")

            if not lst_audio:
                print(f"No audio found for {vinyl_title}")
                continue

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
                    "vinyl_price": vinyl_price,
                    "vinyl_ref": vinyl_ref,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                    "date_extract": pd.Timestamp.now(),
                }

                results = pd.concat(
                    [results, pd.DataFrame(row, index=[0])], ignore_index=True
                )

        print(f"Scrapped {len(results)} items")

    # Upload results to GCP Storage
    save_file(
        df=results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


def scrap_onlyrootsreggae(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Scrap onlyrootsreggae

    Args:
        name_shop (str): name of shop
        conn_id (str): connection ID for the database
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming

    """
    print(f"Scrapping {name_shop}...")

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    # Get shop infos from DB
    df_list_shops = get_specific_shop_links(conn, name_shop)

    # Control if shop is in list of shops
    control_list_shops(name_shop, df_list_shops)

    list_urls = df_list_shops[df_list_shops["name_shop"] == name_shop]["links"].values
    print(f"Scrapping {name_shop} from URLs: {list_urls}")
    conn.close()  # Close the connection to the database

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags article with class=product-miniature
        lst_articles = html.css("article.product-miniature")

        for vinyl in lst_articles[2:4]:
            vinyl_link = vinyl.css_first("link").attributes.get("href")

            # parse HTML
            html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)

            if html_page_vinyl.css_matches("source"):
                vinyl_title = html_page_vinyl.css_first("h1.page-heading").text()
                print(f"Scrapping {vinyl_title}")

                vinyl_image = html_page_vinyl.css_first("img.img-fluid").attributes.get(
                    "src"
                )
                format_vinyl = (
                    vinyl_title.split(" ")[0]
                    .replace(")", "")
                    .replace("(", "")
                    .replace('"', "")
                )

                # price
                vinyl_price = html_page_vinyl.css_first("span.current-price").text()

                # ref
                vinyl_ref = f"{format_vinyl}-{vinyl_link.split('/')[-1].split('-')[0]}"

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
                        "vinyl_price": vinyl_price,
                        "vinyl_ref": vinyl_ref,
                        "mp3_title": mp3_title,
                        "mp3_link": mp3_link,
                        "date_extract": pd.Timestamp.now(),
                    }

                    results = pd.concat(
                        [results, pd.DataFrame(row, index=[0])], ignore_index=True
                    )

        print(f"Scrapped {len(results)} items")

    # Upload results to GCP Storage
    save_file(
        df=results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


def scrap_controltower(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Scrap controltower

    Args:
        name_shop (str): name of shop
        url (str): url to scrap

    """
    print(f"Scrapping {name_shop}...")

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    # Get shop infos from DB
    df_list_shops = get_specific_shop_links(conn, name_shop)

    # Control if shop is in list of shops
    control_list_shops(name_shop, df_list_shops)

    list_urls = df_list_shops[df_list_shops["name_shop"] == name_shop]["links"].values
    print(f"Scrapping {name_shop} from URLs: {list_urls}")
    conn.close()  # Close the connection to the database

    results = pd.DataFrame()

    # parse HTML
    html = HTMLParser(httpx.get(list_urls[0]).text)

    # retrieve all tags article with class=product-miniature
    lst_items = html.css("a.product_img_link")

    # retrieve infos of the 70 first elements
    for vinyl in lst_items[2:4]:
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

            # price
            vinyl_price = html_page_vinyl.css_first("span#our_price_display").text()

            # ref
            vinyl_ref = (
                html_page_vinyl.css_first("p#product_reference")
                .css_first("span")
                .attributes.get("content")
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
                    "vinyl_price": vinyl_price,
                    "vinyl_ref": vinyl_ref,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                    "date_extract": pd.Timestamp.now(),
                }

                results = pd.concat(
                    [results, pd.DataFrame(row, index=[0])], ignore_index=True
                )

    # Upload results to GCP Storage
    save_file(
        df=results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


def scrap_reggaefever(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Scrap reggaefever

    Args:
        name_shop (str): name of shop
        conn_id (str): connection ID for the database
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming

    """
    print(f"Scrapping {name_shop}...")

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    # Get shop infos from DB
    df_list_shops = get_specific_shop_links(conn, name_shop)

    # Control if shop is in list of shops
    control_list_shops(name_shop, df_list_shops)

    list_urls = df_list_shops[df_list_shops["name_shop"] == name_shop]["links"].values
    print(f"Scrapping {name_shop} from URLs: {list_urls}")
    conn.close()  # Close the connection to the database

    results = pd.DataFrame()

    date_ann = [str(i) for i in range(2000, 2050)]

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags tr
        lst_articles = html.css("tr")

        for item in lst_articles[4:8]:
            if item.text().lstrip()[:4] not in date_ann:
                if item.css_matches("td.articleFormat"):
                    format_vinyl = item.css_first("td.articleFormat").text()

                # title
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

                # image
                if item.css_matches("img.articleIcon"):
                    vinyl_image = item.css_first("img.articleIcon").attributes.get(
                        "src"
                    )

                # link
                if item.css_matches("a"):
                    if "articleId" in item.css_first("a").attributes.get("href"):
                        vinyl_link = "https://www.reggaefever.ch/" + item.css_first(
                            "a"
                        ).attributes.get("href")
                        save_link = vinyl_link
                    else:
                        vinyl_link = save_link

                # price
                if item.css_matches("td.price"):
                    if (
                        item.css_first("td.price").text() != ""
                        or item.css_first("td.price").text() != None
                    ):
                        vinyl_price = re.sub(
                            " +",
                            "",
                            item.css_first("td.price")
                            .text()
                            .replace("\n", "")
                            .replace("\t", ""),
                        )
                        save_price = vinyl_price
                    else:
                        vinyl_price = save_price
                else:
                    vinyl_price = save_price

                # ref
                vinyl_ref = vinyl_link.split("=")[-1]

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
                        "vinyl_price": vinyl_price,
                        "vinyl_ref": vinyl_ref,
                        "mp3_title": mp3_title,
                        "mp3_link": mp3_link,
                        "date_extract": pd.Timestamp.now(),
                    }

                    results = pd.concat(
                        [results, pd.DataFrame(row, index=[0])], ignore_index=True
                    )

        print(f"Scrapped {len(results)} items")

    # Upload results to GCP Storage
    save_file(
        df=results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


def scrap_pataterecords(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Scrap pataterecords

    Args:
        name_shop (str): name of shop
        conn_id (str): connection ID for the database
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming

    """
    print(f"Scrapping {name_shop}...")

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    # Get shop infos from DB
    df_list_shops = get_specific_shop_links(conn, name_shop)

    # Control if shop is in list of shops
    control_list_shops(name_shop, df_list_shops)

    list_urls = df_list_shops[df_list_shops["name_shop"] == name_shop]["links"].values
    print(f"Scrapping {name_shop} from URLs: {list_urls}")
    conn.close()  # Close the connection to the database

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags article with class=product-miniature
        lst_articles = html.css("div.img_shop_article")

        for vinyl in lst_articles[2:4]:
            vinyl_image = vinyl.css_first("img").attributes.get("src")
            vinyl_link = vinyl.css_first("a").attributes.get("href")

            # parse HTML
            html_page_vinyl = HTMLParser(httpx.get(vinyl_link).text)

            # if mp3 exist => retreive elements
            if html_page_vinyl.css_matches("audio"):
                vinyl_title = html_page_vinyl.css_first("h1").text()
                print(f"Scrapping {vinyl_title}")

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

                # price
                vinyl_price = html_page_vinyl.css_first("span.price").text()

                # ref
                vinyl_ref = [
                    # span.text().split(": ")[1]
                    f"R-{span.text().split(': ')[1]}"
                    for span in html_page_vinyl.css("span")
                    if span.text().startswith("Ref")
                ][0]

                if not vinyl_ref:
                    vinyl_ref = vinyl_title

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
                        "vinyl_price": vinyl_price,
                        "vinyl_ref": vinyl_ref,
                        "mp3_title": mp3_title,
                        "mp3_link": mp3_link,
                        "date_extract": pd.Timestamp.now(),
                    }

                    results = pd.concat(
                        [results, pd.DataFrame(row, index=[0])], ignore_index=True
                    )

        print(f"Scrapped {len(results)} items")

    # Upload results to GCP Storage
    save_file(
        df=results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


def scrap_toolboxrecords(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Scrap toolboxrecords

    Args:
        name_shop (str): name of shop
        conn_id (str): connection ID for the database
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming

    """
    print(f"Scrapping {name_shop}...")

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    # Get shop infos from DB
    df_list_shops = get_specific_shop_links(conn, name_shop)

    # Control if shop is in list of shops
    control_list_shops(name_shop, df_list_shops)

    list_urls = df_list_shops[df_list_shops["name_shop"] == name_shop]["links"].values
    print(f"Scrapping {name_shop} from URLs: {list_urls}")
    conn.close()  # Close the connection to the database

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)

        # retrieve all tags article with class=product-miniature
        lst_articles = html.css("div.product-cell-thumb")

        for vinyl in lst_articles[2:4]:
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

                print(f"Scrapping {vinyl_title}")

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

                # price
                vinyl_price = re.sub(
                    " +",
                    "",
                    vinyl.css_first("div.product-price")
                    .text()
                    .replace("\n", "")
                    .replace("\t", ""),
                )

                # ref
                vinyl_ref = f"R-{vinyl_link.split('/')[-4]}"

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
                        "vinyl_price": vinyl_price,
                        "vinyl_ref": vinyl_ref,
                        "mp3_title": mp3_title,
                        "mp3_link": mp3_link,
                        "date_extract": pd.Timestamp.now(),
                    }

                    results = pd.concat(
                        [results, pd.DataFrame(row, index=[0])], ignore_index=True
                    )

        print(f"Scrapped {len(results)} items")

    # Upload results to GCP Storage
    save_file(
        df=results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


def scrap_lionvibes(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Scrap lionvibes

    Args:
        name_shop (str): name of shop
        conn_id (str): connection ID for the database
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming

    """
    print(f"Scrapping {name_shop}...")

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    # Get shop infos from DB
    df_list_shops = get_specific_shop_links(conn, name_shop)

    # Control if shop is in list of shops
    control_list_shops(name_shop, df_list_shops)

    list_urls = df_list_shops[df_list_shops["name_shop"] == name_shop]["links"].values
    print(f"Scrapping {name_shop} from URLs: {list_urls}")
    conn.close()  # Close the connection to the database

    results = pd.DataFrame()

    for url in list_urls:

        print(f"Scrapping {url}")

        # parse HTML
        html = HTMLParser(httpx.get(url).text)
        print(f"Parsed HTML from {html}")

        # retrieve all tags article with class=album-block
        # lst_articles = html.css("div.album-block")
        lst_articles = html.css("div.card--card")

        for vinyl in lst_articles[2:4]:

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
            print(f"Scrapping {vinyl_title}")

            format_vinyl = (
                lst_infos[1]
                .text()
                .replace("Format: ", "")
                .replace("Double ", "")
                .replace('"', "")
            )

            # Price
            vinyl_price = re.sub(
                " +",
                "",
                vinyl.css_first("span.price-item")
                .text()
                .replace("\n", "")
                .replace("\t", ""),
            )

            # Ref
            vinyl_ref = f"R-{vinyl_link.split('?')[0].split('-')[-1]}"

            # if vinyl.css_matches("div.col-xs-6"):
            lst_audio = vinyl.css_first("div.card__audio").css(".clip")

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
                    "vinyl_price": vinyl_price,
                    "vinyl_ref": vinyl_ref,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                    "date_extract": pd.Timestamp.now(),
                }

                results = pd.concat(
                    [results, pd.DataFrame(row, index=[0])], ignore_index=True
                )

        print(f"Scrapped {len(results)} items")

    # Upload results to GCP Storage
    save_file(
        df=results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


def scrap_reggaemuseum(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Scrap reggaemuseum

    Args:
        name_shop (str): name of shop
        conn_id (str): connection ID for the database
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming

    """
    print(f"Scrapping {name_shop}...")

    # Connect to DB
    conn = db_connect_postgres(conn_id)

    # Get shop infos from DB
    df_list_shops = get_specific_shop_links(conn, name_shop)

    # Control if shop is in list of shops
    control_list_shops(name_shop, df_list_shops)

    list_urls = df_list_shops[df_list_shops["name_shop"] == name_shop]["links"].values
    print(f"Scrapping {name_shop} from URLs: {list_urls}")
    conn.close()  # Close the connection to the database

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

        for vinyl in lst_articles[2:4]:

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
            print(f"Scrapping {vinyl_title}")

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

            # price
            vinyl_price = html_page_vinyl.css_first("span#our_price_display").text()

            # ref
            vinyl_ref = (
                html_page_vinyl.css_first("p#product_reference")
                .css_first("span")
                .attributes.get("content")
            )

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
                    "vinyl_price": vinyl_price,
                    "vinyl_ref": vinyl_ref,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                    "date_extract": pd.Timestamp.now(),
                }

                results = pd.concat(
                    [results, pd.DataFrame(row, index=[0])], ignore_index=True
                )

        print(f"Scrapped {len(results)} items")

    # Upload results to GCP Storage
    save_file(
        df=results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )
