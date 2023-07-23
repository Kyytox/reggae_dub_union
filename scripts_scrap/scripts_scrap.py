import re
import pandas as pd
import random
import httpx
from selectolax.parser import HTMLParser


async def get_url(client: httpx.AsyncClient, url: str) -> HTMLParser:
    """Get HTML from url"""
    res = await client.get(url)
    return HTMLParser(res.text)


async def scrap_jahwaggysrecords(client: httpx.AsyncClient, name_shop: str, url: str) -> pd.DataFrame:
    results = pd.DataFrame()

    # get format vinyl
    format_vinyl = url[44:46].replace("-", "")
    format_vinyl = "test press" if format_vinyl == "s" else format_vinyl

    # parse HTML
    html = await get_url(client, url)

    # retrieve all tags article with class=product-miniature
    lst_articles = html.css("article.product-miniature")

    async with httpx.AsyncClient(timeout=None) as client2:
        for vinyl in lst_articles[14:]:
            vinyl_title = vinyl.css_first("h3.product-title").text()
            vinyl_image = vinyl.css_first("img").attributes.get("src")
            vinyl_link = vinyl.css_first("a").attributes.get("href")

            # open url link_vinyl for retrieve mp3 link
            html_page_vinyl = await get_url(client2, vinyl_link)
            # parse HTML
            lst_mp3 = html_page_vinyl.css("a.sm2_button")

            # mp3 infos
            for mp3 in lst_mp3:
                mp3_title = mp3.attributes.get("title")
                mp3_link = "https://jahwaggysrecords.com/" + mp3.attributes.get("href")

                row = {
                    "name_shop": name_shop,
                    "format_vinyl": format_vinyl,
                    "vinyl_title": vinyl_title,
                    "vinyl_image": vinyl_image,
                    "vinyl_link": vinyl_link,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                }

                results = pd.concat([results, pd.DataFrame(row, index=[0])])

    return results


async def scrap_onlyrootsreggae(client: httpx.AsyncClient, name_shop: str, url: str) -> pd.DataFrame:
    results = pd.DataFrame()
    # parse HTML
    html = await get_url(client, url)

    # retrieve all tags article with class=product-miniature
    lst_articles = html.css("article.product-miniature")

    async with httpx.AsyncClient(timeout=None) as client2:
        for vinyl in lst_articles:
            vinyl_link = vinyl.css_first("link").attributes.get("href")

            # open url link_vinyl for retrieve mp3 link
            html_page_vinyl = await get_url(client2, vinyl_link)

            if html_page_vinyl.css_matches("source"):
                vinyl_title = html_page_vinyl.css_first("h1.page-heading").text()
                vinyl_image = html_page_vinyl.css_first("img.img-fluid").attributes.get("src")
                format_vinyl = vinyl_title.split(" ")[0].replace(")", "").replace("(", "").replace('"', "")

                # retrieve all mp3
                lst_mp3 = html_page_vinyl.css("source")

                for mp3 in lst_mp3:
                    mp3_title = mp3.attributes.get("title")
                    mp3_link = "https://www.onlyroots-reggae.com" + mp3.attributes.get("src")

                    row = {
                        "name_shop": name_shop,
                        "format_vinyl": format_vinyl,
                        "vinyl_title": vinyl_title,
                        "vinyl_image": vinyl_image,
                        "vinyl_link": vinyl_link,
                        "mp3_title": mp3_title,
                        "mp3_link": mp3_link,
                    }

                results = pd.concat([results, pd.DataFrame(row, index=[0])])

    return results


async def scrap_controltower(client: httpx.AsyncClient, name_shop: str, url: str) -> pd.DataFrame:
    results = pd.DataFrame()
    # get acces to url
    res = httpx.get(url)
    # parse HTML
    html = HTMLParser(res.text)

    # retrieve all tags article with class=product-miniature
    lst_items = html.css("a.product_img_link")

    # retrieve infos of the 70 first elements
    for vinyl in lst_items[:70]:
        vinyl_link = vinyl.attributes.get("href")

        # open url link_vinyl for retrieve mp3 link
        page_vinyl = httpx.get(vinyl_link)

        # parse HTML
        html_page_vinyl = HTMLParser(page_vinyl.text)

        # retrieve infos if tag option exists
        if html_page_vinyl.css_matches("option"):
            vinyl_title = html_page_vinyl.css_first("h1").text()
            vinyl_image = html_page_vinyl.css_first("img#bigpic").attributes.get("src")
            format_vinyl = html_page_vinyl.css_first("option").text().replace(")", "").replace("(", "").replace('"', "")

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
                }

                results = pd.concat([results, pd.DataFrame(row, index=[0])])

    return results


async def scrap_reggaefever(client: httpx.AsyncClient, name_shop: str, url: str) -> pd.DataFrame:
    results = pd.DataFrame()

    date_ann = [str(i) for i in range(2017, 2036)]

    # if function call by customSearch don't skip the firsts articles
    nb_art_no_take = 0 if "generic" in url else 2

    # get HTML
    html = await get_url(client, url)

    # retrieve all tags tr
    lst_articles = html.css("tr")

    for item in lst_articles[nb_art_no_take:]:
        if item.text().lstrip()[:4] not in date_ann:
            if item.css_matches("td.articleFormat"):
                format_vinyl = item.css_first("td.articleFormat").text()

            if item.css_matches("td.artist"):
                vinyl_title = item.css_first("td.artist").text() + " - " + item.css_first("td.title").text()

            if item.css_matches("img.articleIcon"):
                vinyl_image = item.css_first("img.articleIcon").attributes.get("src")

            if item.css_matches("a"):
                vinyl_link = "https://www.reggaefever.ch/" + item.css_first("a").attributes.get("href")

            if item.css_matches("td.title"):
                mp3_title = item.css_first("td.title").text()
            else:
                mp3_title = "version"

            if item.css_matches("a[target=rfplayer]"):
                mp3_link = item.css_first("a[target=rfplayer]").attributes.get("href")

                row = {
                    "name_shop": name_shop,
                    "format_vinyl": format_vinyl,
                    "vinyl_title": vinyl_title,
                    "vinyl_image": vinyl_image,
                    "vinyl_link": vinyl_link,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                }

                results = pd.concat([results, pd.DataFrame(row, index=[0])])

    return results


async def scrap_pataterecords(client: httpx.AsyncClient, name_shop: str, url: str) -> pd.DataFrame:
    results = pd.DataFrame()

    # parse HTML
    html = await get_url(client, url)

    # retrieve all tags article with class=product-miniature
    lst_articles = html.css("div.img_shop_article")

    async with httpx.AsyncClient(timeout=None) as client2:
        for vinyl in lst_articles:
            vinyl_image = vinyl.css_first("img").attributes.get("src")
            vinyl_link = vinyl.css_first("a").attributes.get("href")

            # open url link_vinyl for retrieve mp3 link
            html_page_vinyl = await get_url(client2, vinyl_link)

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
                        }

                        results = pd.concat([results, pd.DataFrame(row, index=[0])])

    return results


async def scrap_toolboxrecords(client: httpx.AsyncClient, name_shop: str, url: str) -> pd.DataFrame:
    results = pd.DataFrame()

    # parse HTML
    html = await get_url(client, url)

    # retrieve all tags article with class=product-miniature
    lst_articles = html.css("div.product-cell-thumb")

    # async with httpx.AsyncClient(timeout=None) as client2:
    for vinyl in lst_articles:
        if vinyl.css_matches("ul.product-track-listing"):
            vinyl_image = vinyl.css_first("img").attributes.get("src")
            vinyl_link = vinyl.css_first("a").attributes.get("href")
            vinyl_title = (
                vinyl.css_first("span.product-name").text()
                + " - "
                + vinyl.css_first("div.product-infos-details").css_first("li").text()
            )

            # Format vinyl
            format_vinyl = vinyl.css_first("div.product-infos-details").css_first("ul").text()
            if '7"' in format_vinyl or "7''" in format_vinyl:
                format_vinyl = "7"
            elif "LP" in format_vinyl or "CD" in format_vinyl:
                format_vinyl = "lp"
            elif "10''" in format_vinyl:
                format_vinyl = "10"
            else:
                format_vinyl = "12"

            if vinyl.css_matches("li.more-tracks-link"):
                # open url link_vinyl for retrieve mp3 link because all mp3 is not is main page
                html_page_vinyl = await get_url(client, vinyl_link)
                div_mp3 = html_page_vinyl.css_first("ul.product-track-listing")
            else:
                div_mp3 = vinyl.css_first("ul.product-track-listing")

            lst_mp3 = div_mp3.css("li")

            for mp3 in lst_mp3[:-1]:
                mp3_title = mp3.css_first("div.track-title").text()
                mp3_link = "https://www.toolboxrecords.com/public/mp3/" + mp3.css_first(
                    "div.track-title"
                ).attributes.get("rel")

                row = {
                    "name_shop": name_shop,
                    "format_vinyl": format_vinyl,
                    "vinyl_title": vinyl_title,
                    "vinyl_image": vinyl_image,
                    "vinyl_link": vinyl_link,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                }

                results = pd.concat([results, pd.DataFrame(row, index=[0])])

    return results


async def scrap_lionvibes(client: httpx.AsyncClient, name_shop: str, url: str) -> pd.DataFrame:
    results = pd.DataFrame()

    # parse HTML
    html = await get_url(client, url)

    # retrieve all tags article with class=album-block
    lst_articles = html.css("div.album-block")

    for vinyl in lst_articles:
        vinyl_image = "https://shop.lionvibes.com" + vinyl.css_first("img").attributes.get("src")
        div_link = vinyl.css("a")
        vinyl_link = "https://shop.lionvibes.com" + div_link[1].attributes.get("href")
        vinyl_title = div_link[1].text()

        artist_name = vinyl.css_first("div.artist-title").css_first("a").text()
        vinyl_title = f"{vinyl_title} - {artist_name}"

        format_vinyl = vinyl.css_first("div.artist-format").css_first("a").text().replace("Double ", "")

        if vinyl.css_matches("div.col-xs-6"):
            div_mp3 = vinyl.css_first("div.col-xs-6")
            lst_mp3 = div_mp3.css("div")

            # range title of track and collect filname attribute for mp3 link
            for track in div_mp3.css("label"):
                mp3_title = track.text()
                mp3_link = "https://shop.lionvibes.com" + lst_mp3[1].attributes.get("filename")

                row = {
                    "name_shop": name_shop,
                    "format_vinyl": format_vinyl,
                    "vinyl_title": vinyl_title,
                    "vinyl_image": vinyl_image,
                    "vinyl_link": vinyl_link,
                    "mp3_title": mp3_title,
                    "mp3_link": mp3_link,
                }

                results = pd.concat([results, pd.DataFrame(row, index=[0])])

    return results


async def scrap_reggaemuseum(client: httpx.AsyncClient, name_shop: str, url: str) -> pd.DataFrame:
    results = pd.DataFrame()
    random_page = 1

    dict_pages = {
        "https://www.reggae-museum.com/shop/14": 22,
        "https://www.reggae-museum.com/shop/15": 42,
        "https://www.reggae-museum.com/shop/16": 13,
        "https://www.reggae-museum.com/shop/18": 2,
    }

    # get random page
    base_url = url.split("-", 2)[0] + "-" + url.split("-", 2)[1]
    end_url = url.split("-", 2)[2]
    random_page = random.randint(1, dict_pages[base_url])
    url = base_url + "-" + end_url + str(random_page)

    # parse HTML
    html = await get_url(client, url)

    # retrieve all tags article with class=product-container
    lst_articles = html.css("div.product-container")
    async with httpx.AsyncClient(timeout=None) as client2:
        for vinyl in lst_articles:
            vinyl_image = vinyl.css_first("img.img-responsive").attributes.get("src")
            vinyl_link = vinyl.css_first("a.product_img_link").attributes.get("href")
            vinyl_title = vinyl.css_first("a.product_img_link").attributes.get("title")

            #  open url link_vinyl for retrieve mp3 link
            html_page_vinyl = await get_url(client2, vinyl_link)

            # list mp3
            lst_mp3 = html_page_vinyl.css("tr")
            if "Audio sample" in lst_mp3[-1].css_first("td").text():
                format_vinyl = re.search(r"\b(7|10|12|lp)\b", vinyl_title.lower()).group(1)

                if lst_mp3[-2].css_matches("a"):
                    track_A = lst_mp3[1].css("td")[-1].text().lstrip().rstrip()
                    link_mp3_A = lst_mp3[-2].css_first("a").attributes.get("href")

                    row = {
                        "name_shop": name_shop,
                        "format_vinyl": format_vinyl,
                        "vinyl_title": vinyl_title,
                        "vinyl_image": vinyl_image,
                        "vinyl_link": vinyl_link,
                        "mp3_title": track_A,
                        "mp3_link": link_mp3_A,
                    }

                    results = pd.concat([results, pd.DataFrame(row, index=[0])])

                if lst_mp3[-1].css_matches("a"):
                    track_B = lst_mp3[4].css("td")[-1].text().lstrip().rstrip()
                    link_mp3_B = lst_mp3[-1].css_first("a").attributes.get("href")

                    row = {
                        "name_shop": name_shop,
                        "format_vinyl": format_vinyl,
                        "vinyl_title": vinyl_title,
                        "vinyl_image": vinyl_image,
                        "vinyl_link": vinyl_link,
                        "mp3_title": track_B,
                        "mp3_link": link_mp3_B,
                    }

                    results = pd.concat([results, pd.DataFrame(row, index=[0])])

    return results
