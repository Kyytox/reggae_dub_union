"""
regroup all functions to scrap vinyls
Each function scrap one shop

"""

import time
import re
import pandas as pd
import random
import httpx
from selectolax.parser import HTMLParser


from airflow.models import Variable

from utils.db_connect import (
    db_connect_postgres,
    get_shop_infos,
    get_shops_links,
)

from utils.utils_gcp_storage import upload_blob


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


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicates from DataFrame

    Args:
        df (pd.DataFrame): DataFrame to remove duplicates from

    Returns:
        pd.DataFrame: DataFrame without duplicates
    """
    return df.drop_duplicates(subset=["vinyl_title", "vinyl_ref", "mp3_title"])


def read_html_page(url: str) -> HTMLParser:
    """
    Read HTML page from URL with retry logic

    Args:
        url (str): URL to read

    Returns:
        HTMLParser: Parsed HTML page
    """
    try:
        # First attempt without specifying timeout
        response = httpx.get(url)
        response.raise_for_status()
        return HTMLParser(response.text)
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        print(f"First attempt failed for {url}: {e}. Retrying with timeout...")
        try:
            # Second attempt with timeout
            response = httpx.get(url, timeout=8)
            response.raise_for_status()
            return HTMLParser(response.text)
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Error fetching {url} after retry: {e}")
            raise Exception(f"Failed to fetch {url} after multiple attempts: {e}")


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

    df_results = pd.DataFrame()
    max_pages = 400  # Maximum number of pages to scrap

    # Get shop infos from DB
    df_infos = get_shop_infos(conn_id, name_shop)

    # Get shops links
    lst_urls = get_shops_links(df_infos)

    # get first vinyl_reference
    vinyl_reference = df_infos["vinyl_reference"].iloc[0]

    # define max_pages to scrap
    if vinyl_reference is not None:
        max_pages = 2

    for base_url in lst_urls:
        print(f"Scrapping {name_shop} from URL: {base_url}")

        # initialize variables
        top_break = False
        pg = 1

        while pg < max_pages:

            # add number page to url
            url = base_url + f"{pg}"
            print(f"Scrapping {url}")

            # parse HTML
            html = read_html_page(url)

            # find section class page-not-found
            if html.css_matches("section.page-not-found"):
                print("Page not found. Pass to next Url.")
                break

            # get format vinyl
            vinyl_format = url[44:46].replace("-", "")
            vinyl_format = "test press" if vinyl_format == "s" else vinyl_format

            # retrieve all tags article with class=product-miniature
            lst_articles = html.css("article.product-miniature")

            for vinyl in lst_articles:
                vinyl_link = vinyl.css_first("a").attributes.get("href")

                # parse HTML
                html_page_vinyl = read_html_page(vinyl_link)

                vinyl_title = html_page_vinyl.css_first("h1.product_name").text()
                vinyl_image = html_page_vinyl.css_first("img").attributes.get("src")
                vinyl_price = html_page_vinyl.css_first("span.price").text()

                print(f"Scrapping {vinyl_title}")

                div_tabs = html_page_vinyl.css_first("div.tabs")

                if div_tabs.css_matches("div.product-reference"):
                    vinyl_ref = (
                        div_tabs.css_first("div.product-reference")
                        .css_first("span")
                        .text()
                    )
                else:
                    vinyl_ref = vinyl_title

                # control if vinyl_ref already exists in table vinyls
                if vinyl_ref == vinyl_reference:
                    top_break = True
                    print(f"Data already exists for {vinyl_ref}. Stop scrapping.")
                    break

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
                for mp3 in range(len(lst_mp3)):
                    mp3_title = lst_titles[mp3].text()
                    mp3_link = "https://jahwaggysrecords.com" + lst_mp3[
                        mp3
                    ].attributes.get("src")

                    row = {
                        "name_shop": name_shop,
                        "vinyl_format": vinyl_format,
                        "vinyl_title": vinyl_title,
                        "vinyl_image": vinyl_image,
                        "vinyl_link": vinyl_link,
                        "vinyl_price": vinyl_price,
                        "vinyl_ref": vinyl_ref,
                        "mp3_title": mp3_title,
                        "mp3_link": mp3_link,
                        "date_extract": pd.Timestamp.now(),
                    }

                    df_results = pd.concat(
                        [df_results, pd.DataFrame(row, index=[0])], ignore_index=True
                    )

            print(f"Scrapped {len(df_results)} items from page {pg}")

            if top_break:
                print("Top break reached. Stop scrapping.")
                break

            pg += 1

    print(f"Scrapped {len(df_results)} items")

    # Remove duplicates
    df_results = remove_duplicates(df_results)

    print(f"Removed duplicates. {len(df_results)} items left.")
    df_results.to_csv(f"./{name_shop}.csv", index=False)

    save_file(
        df=df_results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


def scrap_onlyrootsreggae(
    name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
) -> None:
    # Upload df_results to GCP Storage
    """
    Scrap onlyrootsreggae

    Args:
        name_shop (str): name of shop
        conn_id (str): connection ID for the database
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming

    """
    print(f"Scrapping {name_shop}...")

    df_results = pd.DataFrame()
    max_pages = 100  # Maximum number of pages to scrap

    # Get shop infos from DB
    df_infos = get_shop_infos(conn_id, name_shop)

    # Get shops links
    lst_urls = get_shops_links(df_infos)
    print(f"Scrapping {name_shop} from URLs: {lst_urls}")

    # get first vinyl_reference
    vinyl_reference = df_infos["vinyl_reference"].iloc[0]

    # define max_pages to scrap
    if vinyl_reference is not None:
        max_pages = 5

    for base_url in lst_urls:

        # initialize variables
        top_break = False
        pg = 1

        while pg < max_pages:

            # add number page to url
            url = base_url.replace("=X", f"={pg}")
            print(f"Scrapping {url}")

            # parse HTML
            html = read_html_page(url)

            # find section class page-not-found
            if html.css_matches("section.page-not-found"):
                print("Page not found. Pass to next Url.")
                break

            # retrieve all tags article with class=product-miniature
            lst_articles = html.css("article.product-miniature")

            for vinyl in lst_articles:
                vinyl_link = vinyl.css_first("link").attributes.get("href")

                # parse HTML
                html_page_vinyl = read_html_page(vinyl_link)

                if html_page_vinyl.css_matches("source"):
                    vinyl_title = html_page_vinyl.css_first("h1.page-heading").text()
                    print(f"Scrapping {vinyl_title}")

                    vinyl_image = html_page_vinyl.css_first(
                        "img.img-fluid"
                    ).attributes.get("src")

                    vinyl_format = (
                        vinyl_title.split(" ")[0]
                        .replace(")", "")
                        .replace("(", "")
                        .replace('"', "")
                    )

                    # price
                    vinyl_price = html_page_vinyl.css_first("span.current-price").text()

                    # ref
                    vinyl_ref = (
                        f"{vinyl_format}-{vinyl_link.split('/')[-1].split('-')[0]}"
                    )

                    # control if vinyl_ref already exists in table vinyls
                    if vinyl_ref == vinyl_reference:
                        top_break = True
                        print(f"Data already exists for {vinyl_ref}. Stop scrapping.")
                        break

                    # retrieve all mp3
                    lst_mp3 = html_page_vinyl.css("source")

                    for mp3 in lst_mp3:
                        mp3_title = mp3.attributes.get("title")
                        mp3_link = (
                            "https://www.onlyroots-reggae.com"
                            + mp3.attributes.get("src")
                        )

                        row = {
                            "name_shop": name_shop,
                            "vinyl_format": vinyl_format,
                            "vinyl_title": vinyl_title,
                            "vinyl_image": vinyl_image,
                            "vinyl_link": vinyl_link,
                            "vinyl_price": vinyl_price,
                            "vinyl_ref": vinyl_ref,
                            "mp3_title": mp3_title,
                            "mp3_link": mp3_link,
                            "date_extract": pd.Timestamp.now(),
                        }

                        df_results = pd.concat(
                            [df_results, pd.DataFrame(row, index=[0])],
                            ignore_index=True,
                        )
            print(f"Scrapped {len(df_results)} items from page {pg}")

            if top_break:
                print("Top break reached. Stop scrapping.")
                break

            pg += 1

            # Sleep to avoid being blocked by the website
            if pg % 5 == 0:
                time.sleep(30)

    print(f"Scrapped {len(df_results)} items")

    # Remove duplicates
    df_results = remove_duplicates(df_results)

    print(f"Removed duplicates. {len(df_results)} items left.")
    df_results.to_csv(f"./{name_shop}.csv", index=False)

    # Upload results to GCP Storage
    save_file(
        df=df_results,
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

    df_results = pd.DataFrame()
    max_elements = 3000  # Maximum number of elements to scrap (shop has no pagination)

    # Get shop infos from DB
    df_infos = get_shop_infos(conn_id, name_shop)

    # Get shops links
    lst_urls = get_shops_links(df_infos)
    print(f"Scrapping {name_shop} from URLs: {lst_urls}")

    # get first vinyl_reference
    vinyl_reference = df_infos["vinyl_reference"].iloc[0]

    # define max_pages to scrap
    if vinyl_reference is not None:
        max_elements = 50

    # parse HTML
    html = HTMLParser(httpx.get(lst_urls[0]).text)

    # retrieve all tags article with class=product-miniature
    lst_items = html.css("a.product_img_link")
    print(f"Found {len(lst_items)} items to scrap.")

    # retrieve infos of the 70 first elements
    for vinyl in lst_items[:max_elements]:
        vinyl_link = vinyl.attributes.get("href")

        # parse HTML
        html_page_vinyl = read_html_page(vinyl_link)

        # retrieve infos if tag option exists
        if html_page_vinyl.css_matches("option"):

            # get vinyl title
            vinyl_title = html_page_vinyl.css_first("h1").text()
            print(f"Scrapping {vinyl_title}")

            # ref
            vinyl_ref = (
                html_page_vinyl.css_first("p#product_reference")
                .css_first("span")
                .attributes.get("content")
            )

            # control if vinyl_ref already exists in table vinyls
            if vinyl_ref == vinyl_reference:
                print(f"Data already exists for {vinyl_ref}. Stop scrapping.")
                break

            # retrieve Image
            vinyl_image = html_page_vinyl.css_first("img#bigpic").attributes.get("src")

            # retrieve format vinyl
            vinyl_format = (
                html_page_vinyl.css_first("option")
                .text()
                .replace(")", "")
                .replace("(", "")
                .replace('"', "")
            )

            # price
            vinyl_price = html_page_vinyl.css_first("span#our_price_display").text()

            # retrieve all mp3
            lst_mp3 = html_page_vinyl.css("source")

            for mp3 in lst_mp3:
                mp3_title = mp3.attributes.get("title")
                mp3_link = mp3.attributes.get("src")

                row = {
                    "name_shop": name_shop,
                    "vinyl_format": vinyl_format,
                    "vinyl_title": vinyl_title,
                    "vinyl_image": vinyl_image,
                    "vinyl_link": vinyl_link,
                    "vinyl_price": vinyl_price,
                    "vinyl_ref": vinyl_ref,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                    "date_extract": pd.Timestamp.now(),
                }

                df_results = pd.concat(
                    [df_results, pd.DataFrame(row, index=[0])], ignore_index=True
                )

    print(f"Scrapped {len(df_results)} items")

    # Remove duplicates
    df_results = remove_duplicates(df_results)

    print(f"Removed duplicates. {len(df_results)} items left.")
    df_results.to_csv(f"./{name_shop}.csv", index=False)

    # Upload df_results to GCP Storage
    save_file(
        df=df_results,
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

    df_results = pd.DataFrame()
    max_pages = 600  # Maximum number of pages to scrap

    # Get shop infos from DB
    df_infos = get_shop_infos(conn_id, name_shop)

    # Get shops links
    lst_urls = get_shops_links(df_infos)
    print(f"Scrapping {name_shop} from URLs: {lst_urls}")

    # get first vinyl_reference
    vinyl_reference = df_infos["vinyl_reference"].iloc[0]

    # define max_pages to scrap
    if vinyl_reference is not None:
        max_pages = 2

    date_ann = [str(i) for i in range(2000, 2050)]

    for base_url in lst_urls:

        # initialize variables
        top_break = False
        pg = 1

        while pg < max_pages:

            # add number page to url
            url = base_url + f"{pg}"
            print(f"Scrapping {url}")

            # parse HTML
            html = read_html_page(url)

            # Control if we are on the right page
            if html.css_matches("a.pageLinkCurrent"):
                if int(html.css_first("a.pageLinkCurrent").text()) < pg:
                    print("Page not found. Pass to next Url.")
                    break

            # retrieve all tags tr
            lst_articles = html.css("tr")

            for item in lst_articles[1:]:
                if item.text().lstrip()[:4] not in date_ann:
                    if item.css_matches("td.articleFormat"):
                        vinyl_format = item.css_first("td.articleFormat").text()

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

                    print(f"Scrapping {vinyl_title}")

                    # link
                    if item.css_matches("a"):
                        if "articleId" in item.css_first("a").attributes.get("href"):
                            vinyl_link = "https://www.reggaefever.ch/" + item.css_first(
                                "a"
                            ).attributes.get("href")
                            save_link = vinyl_link
                        else:
                            vinyl_link = save_link

                    # ref
                    vinyl_ref = vinyl_link.split("=")[-1]

                    # control if vinyl_ref already exists in table vinyls
                    if vinyl_ref == vinyl_reference:
                        print(f"Data already exists for {vinyl_ref}. Stop scrapping.")
                        break

                    # image
                    if item.css_matches("img.articleIcon"):
                        vinyl_image = item.css_first("img.articleIcon").attributes.get(
                            "src"
                        )

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
                            "vinyl_format": vinyl_format,
                            "vinyl_title": vinyl_title,
                            "vinyl_image": vinyl_image,
                            "vinyl_link": vinyl_link,
                            "vinyl_price": vinyl_price,
                            "vinyl_ref": vinyl_ref,
                            "mp3_title": mp3_title,
                            "mp3_link": mp3_link,
                            "date_extract": pd.Timestamp.now(),
                        }

                        df_results = pd.concat(
                            [df_results, pd.DataFrame(row, index=[0])],
                            ignore_index=True,
                        )

            print(f"Scrapped {len(df_results)} items from page {pg}")

            if top_break:
                print("Top break reached. Stop scrapping.")
                break

            pg += 1

    print(f"Scrapped {len(df_results)} items")

    # Remove duplicates
    df_results = remove_duplicates(df_results)

    print(f"Removed duplicates. {len(df_results)} items left.")
    df_results.to_csv(f"./{name_shop}.csv", index=False)

    # Upload df_results to GCP Storage
    save_file(
        df=df_results,
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

    df_results = pd.DataFrame()
    max_pages = 400  # Maximum number of pages to scrap

    # Get shop infos from DB
    df_infos = get_shop_infos(conn_id, name_shop)

    # Get shops links
    lst_urls = get_shops_links(df_infos)
    print(f"Scrapping {name_shop} from URLs: {lst_urls}")

    # get first vinyl_reference
    vinyl_reference = df_infos["vinyl_reference"].iloc[0]

    # define max_pages to scrap
    if vinyl_reference is not None:
        max_pages = 2

    for base_url in lst_urls:

        # initialize variables
        top_break = False
        pg = 1

        while pg < max_pages:

            # add number page to url
            url = base_url.replace("X/", f"{pg}/")
            print(f"Scrapping {url}")

            # parse HTML
            html = read_html_page(url)

            # find section class page-not-found
            if html.css_matches("h1"):
                if html.css_first("h1").text().startswith("Oooups"):
                    print("Page not found. Pass to next Url.")
                    break

            # retrieve all tags article with class=product-miniature
            lst_articles = html.css("div.img_shop_article")

            for vinyl in lst_articles:
                vinyl_image = vinyl.css_first("img").attributes.get("src")
                vinyl_link = vinyl.css_first("a").attributes.get("href")

                # price
                if vinyl.css_matches("span.shop_px_stock"):
                    vinyl_price = vinyl.css_first("span.shop_px_stock").text()
                elif vinyl.css_matches("span.shop_px"):
                    vinyl_price = vinyl.css_first("span.shop_px").text()
                elif vinyl.css_matches("span.px_article_indisponible"):
                    vinyl_price = vinyl.css_first("span.px_article_indisponible").text()
                else:
                    vinyl_price = "0.00 €"

                # parse HTML
                html_page_vinyl = read_html_page(vinyl_link)

                # if mp3 exist => retreive elements
                if html_page_vinyl.css_matches("audio"):
                    vinyl_title = html_page_vinyl.css_first("h1").text()
                    # print(f"Scrapping {vinyl_title}")

                    # ref
                    vinyl_ref = [
                        f"R-{span.text().split(': ')[1]}"
                        for span in html_page_vinyl.css("span")
                        if span.text().startswith("Ref")
                    ]
                    vinyl_ref = vinyl_ref[0] if vinyl_ref else None

                    if not vinyl_ref:
                        vinyl_ref = vinyl_title

                    # control if vinyl_ref already exists in table vinyls
                    if vinyl_ref == vinyl_reference:
                        top_break = True
                        print(f"Data already exists for {vinyl_ref}. Stop scrapping.")
                        break

                    # list mp3
                    div_mp3 = html_page_vinyl.css_first("div#traclist")
                    lst_mp3 = div_mp3.css("div")

                    # Format vinyl
                    div_format = html_page_vinyl.css_first("div#caracteristic")
                    vinyl_format = div_format.css_first("span").text()

                    if "7" in vinyl_format:
                        vinyl_format = "7"
                    elif "LP" in vinyl_format:
                        vinyl_format = "lp"
                    elif len(lst_mp3) < 5:
                        vinyl_format = "10"
                    else:
                        vinyl_format = "12"

                    for mp3 in lst_mp3[:-1]:
                        if mp3.css_matches("source"):
                            mp3_title = mp3.text().split("\n")[-1]
                            mp3_link = mp3.css_first("source").attributes.get("src")

                        row = {
                            "name_shop": name_shop,
                            "vinyl_format": vinyl_format,
                            "vinyl_title": vinyl_title,
                            "vinyl_image": vinyl_image,
                            "vinyl_link": vinyl_link,
                            "vinyl_price": vinyl_price,
                            "vinyl_ref": vinyl_ref,
                            "mp3_title": mp3_title,
                            "mp3_link": mp3_link,
                            "date_extract": pd.Timestamp.now(),
                        }

                        df_results = pd.concat(
                            [df_results, pd.DataFrame(row, index=[0])],
                            ignore_index=True,
                        )

            if top_break:
                print("Top break reached. Stop scrapping.")
                break

            pg += 1

            # Sleep to avoid being blocked by the website
            if pg % 5 == 0:
                time.sleep(45)

        df_results.to_csv(f"./{name_shop}_{vinyl_format}.csv", index=False)

    print(f"Scrapped {len(df_results)} items")

    # Remove duplicates
    df_results = remove_duplicates(df_results)

    print(f"Removed duplicates. {len(df_results)} items left.")
    df_results.to_csv(f"./{name_shop}.csv", index=False)

    # Upload df_results to GCP Storage
    save_file(
        df=df_results,
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

    df_results = pd.DataFrame()
    max_pages = 100  # Maximum number of pages to scrap

    # Get shop infos from DB
    df_infos = get_shop_infos(conn_id, name_shop)

    # Get shops links
    lst_urls = get_shops_links(df_infos)
    print(f"Scrapping {name_shop} from URLs: {lst_urls}")

    # get first vinyl_reference
    vinyl_reference = df_infos["vinyl_reference"].iloc[0]

    # define max_pages to scrap
    if vinyl_reference is not None:
        max_pages = 2

    for base_url in lst_urls:

        # initialize variables
        top_break = False
        pg = 1

        while pg < max_pages:

            # add number page to url
            url = base_url.replace("=X", f"={pg}")
            print(f"Scrapping {url}")

            # parse HTML
            html = read_html_page(url)

            # find section class page-not-found
            if html.css_matches("h2.title"):
                if "No products" in html.css_first("h2.title").text():
                    print("Page not found. Pass to next Url.")
                    break

            # retrieve all tags article with class=album-block
            # lst_articles = html.css("div.album-block")
            lst_articles = html.css("div.card--card")

            for vinyl in lst_articles:

                # Image
                vinyl_image = "https:" + vinyl.css_first("img").attributes.get("src")

                # Link + Title
                div_link = vinyl.css("a")
                vinyl_link = "https:" + div_link[1].attributes.get("href")

                # Ref
                vinyl_ref = f"R-{vinyl_link.split('?')[0].split('-')[-1]}"

                # control if vinyl_ref already exists in table vinyls
                if vinyl_ref == vinyl_reference:
                    top_break = True
                    print(f"Data already exists for {vinyl_ref}. Stop scrapping.")
                    break

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

                vinyl_format = (
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

                # Audios
                if vinyl.css_matches("div.card__audio"):
                    lst_audio = vinyl.css_first("div.card__audio").css(".clip")
                else:
                    print(f"No audio found for {vinyl_title}")
                    continue

                # range title of track and collect filname attribute for mp3 link
                for track in lst_audio:
                    mp3_title = track.css_first("strong").text()
                    mp3_link = "https://shop.lionvibes.com" + track.css_first(
                        "source"
                    ).attributes.get("src")

                    row = {
                        "name_shop": name_shop,
                        "vinyl_format": vinyl_format,
                        "vinyl_title": vinyl_title,
                        "vinyl_image": vinyl_image,
                        "vinyl_link": vinyl_link,
                        "vinyl_price": vinyl_price,
                        "vinyl_ref": vinyl_ref,
                        "mp3_title": mp3_title,
                        "mp3_link": mp3_link,
                        "date_extract": pd.Timestamp.now(),
                    }

                    df_results = pd.concat(
                        [df_results, pd.DataFrame(row, index=[0])], ignore_index=True
                    )

            if top_break:
                print("Top break reached. Stop scrapping.")
                break

            pg += 1

            # Sleep to avoid being blocked by the website
            if pg % 5 == 0:
                time.sleep(60)

    print(f"Scrapped {len(df_results)} items")

    # Remove duplicates
    df_results = remove_duplicates(df_results)

    print(f"Removed duplicates. {len(df_results)} items left.")
    df_results.to_csv(f"./{name_shop}.csv", index=False)

    # Upload df_results to GCP Storage
    save_file(
        df=df_results,
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

    df_results = pd.DataFrame()
    max_pages = 53  # Maximum number of pages to scrap

    # Get shop infos from DB
    df_infos = get_shop_infos(conn_id, name_shop)

    # Get shops links
    lst_urls = get_shops_links(df_infos)
    print(f"Scrapping {name_shop} from URLs: {lst_urls}")

    # get first vinyl_reference
    vinyl_reference = df_infos["vinyl_reference"].iloc[0]

    # define max_pages to scrap
    if vinyl_reference is not None:
        max_pages = 2

    for base_url in lst_urls:

        # initialize variables
        top_break = False
        pg = 1

        while pg < max_pages:

            # add number page to url
            url = base_url + f"{pg}"
            print(f"Scrapping {url}")

            # parse HTML
            html = read_html_page(url)

            # retrieve all tags article with class=product-miniature
            lst_articles = html.css("div.product-cell-thumb")

            if len(lst_articles) == 0:
                print("No articles found. Pass to next Url.")
                break

            for vinyl in lst_articles:
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

                    # ref
                    vinyl_ref = f"R-{vinyl_link.split('/')[-4]}"

                    # control if vinyl_ref already exists in table vinyls
                    if vinyl_ref == vinyl_reference:
                        top_break = True
                        print(f"Data already exists for {vinyl_ref}. Stop scrapping.")
                        break

                    # Format vinyl
                    vinyl_format = (
                        vinyl.css_first("div.product-infos-details")
                        .css_first("ul")
                        .text()
                    )
                    if '7"' in vinyl_format or "7''" in vinyl_format:
                        vinyl_format = "7"
                    elif "LP" in vinyl_format or "CD" in vinyl_format:
                        vinyl_format = "LP"
                    elif "10''" in vinyl_format:
                        vinyl_format = "10"
                    else:
                        vinyl_format = "12"

                    # price
                    vinyl_price = re.sub(
                        " +",
                        "",
                        vinyl.css_first("div.product-price")
                        .text()
                        .replace("\n", "")
                        .replace("\t", ""),
                    )

                    if vinyl.css_matches("li.more-tracks-link"):
                        # open url link_vinyl for retrieve mp3 link because all mp3 is not is main page
                        # parse HTML
                        html_page_vinyl = read_html_page(vinyl_link)

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
                            "vinyl_format": vinyl_format,
                            "vinyl_title": vinyl_title,
                            "vinyl_image": vinyl_image,
                            "vinyl_link": vinyl_link,
                            "vinyl_price": vinyl_price,
                            "vinyl_ref": vinyl_ref,
                            "mp3_title": mp3_title,
                            "mp3_link": mp3_link,
                            "date_extract": pd.Timestamp.now(),
                        }

                        df_results = pd.concat(
                            [df_results, pd.DataFrame(row, index=[0])],
                            ignore_index=True,
                        )

            if top_break:
                print("Top break reached. Stop scrapping.")
                break

            pg += 1

    print(f"Scrapped {len(df_results)} items")

    # Remove duplicates
    df_results = remove_duplicates(df_results)

    print(f"Removed duplicates. {len(df_results)} items left.")
    df_results.to_csv(f"./{name_shop}.csv", index=False)

    # Upload df_results to GCP Storage
    save_file(
        df=df_results,
        name_shop=name_shop,
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )


# def scrap_reggaemuseum(
#     name_shop: str, conn_id: str, bucket_name: str, time_file_name: str
# ) -> None:
#     """
#     Scrap reggaemuseum

#     Args:
#         name_shop (str): name of shop
#         conn_id (str): connection ID for the database
#         bucket_name (str): name of the GCP Storage bucket
#         time_file_name (str): timestamp for file naming

#     """
#     print(f"Scrapping {name_shop}...")

#     df_results = pd.DataFrame()
#     max_pages = 150  # Maximum number of pages to scrap

#     # Get shop infos from DB
#     df_infos = get_shop_infos(conn_id, name_shop)

#     # Get shops links
#     lst_urls = get_shops_links(df_infos)
#     print(f"Scrapping {name_shop} from URLs: {lst_urls}")

#     # get first vinyl_reference
#     vinyl_reference = df_infos["vinyl_reference"].iloc[0]

#     # define max_pages to scrap
#     vinyl_reference = "10rp001"  #! Test
#     if vinyl_reference is not None:
#         max_pages = 2

#     # random_page = 1

#     # dict_pages = {
#     #     "https://www.reggae-museum.com/shop/14": 22,
#     #     "https://www.reggae-museum.com/shop/15": 42,
#     #     "https://www.reggae-museum.com/shop/16": 13,
#     #     "https://www.reggae-museum.com/shop/18": 2,
#     # }

#     # # get random page
#     # base_url = url.split("-", 2)[0] + "-" + url.split("-", 2)[1]
#     # end_url = url.split("-", 2)[2]
#     # random_page = random.randint(1, dict_pages[base_url])
#     # url = base_url + "-" + end_url + str(random_page)

#     for base_url in lst_urls:

#         # initialize variables
#         top_break = False
#         i = 32

#         while i < 35:

#             # add number page to url
#             url = base_url.replace("-X", f"-{i}")
#             print(f"Scrapping {url}")

#             # parse HTML
#             html = read_html_page(url)

#             # retrieve all tags article with class=album-block
#             lst_articles = html.css("div.product-container")
#             print(f"Found {len(lst_articles)} items to scrap.")

#             for vinyl in lst_articles[:4]:

#                 vinyl_image = vinyl.css_first("img.img-responsive").attributes.get(
#                     "src"
#                 )
#                 vinyl_link = vinyl.css_first("a.product_img_link").attributes.get(
#                     "href"
#                 )

#                 vinyl_title = re.sub(
#                     " +",
#                     " ",
#                     vinyl.css_first("a.product-name")
#                     .text()
#                     .replace("\n", " ")
#                     .replace("\t", " "),
#                 )
#                 print(f"Scrapping {vinyl_title}")

#                 #  open url link_vinyl for retrieve mp3 link
#                 html_page_vinyl = read_html_page(vinyl_link)

#                 # ref
#                 vinyl_ref = (
#                     html_page_vinyl.css_first("p#product_reference")
#                     .css_first("span")
#                     .attributes.get("content")
#                 )

#                 # control if vinyl_ref already exists in table vinyls
#                 if vinyl_ref == vinyl_reference:
#                     top_break = True
#                     print(f"Data already exists for {vinyl_ref}. Stop scrapping.")
#                     break

#                 # Extract format from title
#                 if re.search(r"\b(7|10|12|lp|LP)\b", vinyl_title):
#                     vinyl_format = re.search(r"\b(7|10|12|lp|LP)\b", vinyl_title).group(
#                         1
#                     )
#                 else:
#                     vinyl_format = "12"

#                 div_content = html_page_vinyl.css_first("section.page-product-box")

#                 lst_infos = re.sub(
#                     " +", " ", div_content.text().replace("\n", " ").replace("\t", " ")
#                 ).split("] ")

#                 # get artitst if br.text contains "Artist")
#                 lst_articles = [
#                     item.split(": ")[1].split("[")[0].strip()
#                     for item in lst_infos
#                     if "Artist" in item
#                 ]

#                 # get Title if br.text contains "Title"
#                 lst_titles = [
#                     item.split(": ")[1].split("[")[0].strip()
#                     for item in lst_infos
#                     if "Title" in item
#                 ]

#                 # price
#                 vinyl_price = html_page_vinyl.css_first("span#our_price_display").text()

#                 # get audio
#                 lst_mp3 = div_content.css("audio")

#                 for i in range(len(lst_mp3)):
#                     mp3_title = lst_titles[i]
#                     mp3_link = lst_mp3[i].css_first("source").attributes.get("src")

#                     row = {
#                         "name_shop": name_shop,
#                         "vinyl_format": vinyl_format,
#                         "vinyl_title": vinyl_title,
#                         "vinyl_image": vinyl_image,
#                         "vinyl_link": vinyl_link,
#                         "vinyl_price": vinyl_price,
#                         "vinyl_ref": vinyl_ref,
#                         "mp3_title": mp3_title,
#                         "mp3_link": mp3_link,
#                         "date_extract": pd.Timestamp.now(),
#                     }

#                     df_results = pd.concat(
#                         [df_results, pd.DataFrame(row, index=[0])], ignore_index=True
#                     )

#             if top_break:
#                 print("Top break reached. Stop scrapping.")
#                 break
#             i += 1

#         return  #! Test

#     print(f"Scrapped {len(df_results)} items")
#     return

#     # Upload df_results to GCP Storage
#     save_file(
#         df=df_results,
#         name_shop=name_shop,
#         bucket_name=bucket_name,
#         time_file_name=time_file_name,
#     )
