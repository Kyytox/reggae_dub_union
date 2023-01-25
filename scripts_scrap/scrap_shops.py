import httpx 
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import csv
import time
import random
import os
from urllib.request import urlretrieve
from mutagen.mp3 import MP3

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

import asyncio
import nest_asyncio
nest_asyncio.apply()

@dataclass
class Vinyl:
    name_shop: str
    format_vinyl: str
    vinyl_title: str
    vinyl_image: str
    vinyl_link: str
    mp3_title: str
    mp3_link: str


urls_jahwaggys = ["https://jahwaggysrecords.com/fr/5-brand-new-7-vinyl-selection",
"https://jahwaggysrecords.com/fr/6-brand-new-10-vinyl-selection",
"https://jahwaggysrecords.com/fr/7-brand-new-12-vinyl-selection",
"https://jahwaggysrecords.com/fr/8-brand-new-lp-vinyl-selection",
"https://jahwaggysrecords.com/fr/18-test-press-selection"]


url_controltower = "https://controltower.fr/fr/"

urls_onlyrootsreggae = ["https://www.onlyroots-reggae.com/fr/21-singles-7-45t/s-1/?page=1&order=product.date_add.desc",
"https://www.onlyroots-reggae.com/fr/20-maxis-12-10/s-1/?page=1&order=product.date_add.desc", 
"https://www.onlyroots-reggae.com/fr/17-albums-lp-33t/s-1/?page=1&order=product.date_add.desc"]


urls_reggaefever = ["https://www.reggaefever.ch/catalog?format=7&sort=relDate_riddim",
"https://www.reggaefever.ch/catalog?format=10&sort=relDate_riddim",
"https://www.reggaefever.ch/catalog?format=12&sort=relDate_riddim"]


urls_deeprootsreggae = ["http://www.deeprootsreggaeshop.com/epages/300210.sf/en_GB/?ViewAction=View&ObjectID=10252615&PageSize=50&Page=1",
"http://www.deeprootsreggaeshop.com/epages/300210.sf/en_GB/?ViewAction=View&ObjectID=10252615&PageSize=50&Page=2"]


urls_rastavibes = ["https://www.rastavibes.net/reggae-shop/?lang=fr&p=home&format=7p&show=news&since=30",
"https://www.rastavibes.net/reggae-shop/?lang=fr&p=home&format=10p&show=news&since=30",
"https://www.rastavibes.net/reggae-shop/?lang=fr&p=home&format=12p&show=news&since=30",
"https://www.rastavibes.net/reggae-shop/?lang=fr&p=home&format=lp&show=news&since=30"]


urls_pataterecords = ["https://www.patate-records.com/shop/1/1/1/type/1/",
"https://www.patate-records.com/shop/1/1/1/type/2/",
"https://www.patate-records.com/shop/1/1/1/type/3/"]



urls_toolboxrecords = ["https://www.toolboxrecords.com/fr/catalog/list/categoryID/3/item_nbr/60"]



urls_lionvibes = ["https://shop.lionvibes.com/search.php?mode=quicksearch&search_string=&format=7&decade=&pressing=&period=&page=1&sort_by=created_desc",
"https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by=created_desc&search_string=&format=10&decade=&pressing=&period=&page=1&sort_by=created_desc",
"https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by=created_desc&sort_by=created_desc&search_string=&format=12&decade=&pressing=&period=&page=1",
"https://shop.lionvibes.com/search.php?mode=quicksearch&sort_by=created_desc&sort_by=created_desc&search_string=&format=lp&decade=&pressing=&period=&page=1"]



urls_reggaemuseum = [f"https://www.reggae-museum.com/shop/15-ska-rocksteady-roots?n=60&orderby=position&orderway=asc&p={random.randint(1, 42)}",
f"https://www.reggae-museum.com/shop/14-rub-a-dub-early-digital?id_category=14&n=60&p={random.randint(1, 21)}",
f"https://www.reggae-museum.com/shop/16-dancehall-new-roots?n=60&orderby=position&orderway=asc&p={random.randint(1, 12)}",
f"https://www.reggae-museum.com/shop/18-lp-albums?p={random.randint(1, 2)}"]


# urls_reggaecouk = []
# urls_unearthedsounds = ["https://www.unearthedsounds.co.uk/stream/reggae"]
# urls_reggaeduborg = ["https://www.reggaedub.org/fr/14-7?page=1"]





async def scrap_jahwaggysrecords(client, url):
    print('url: ', url)
    results = []

    # reggea Shop name
    name_shop = "jahwaggysrecords.com"

    # set vinyl format based on url info
    format_vinyl_url = url[44:46]
    if format_vinyl_url == "7-":
        format_vinyl = "7"
    elif format_vinyl_url == "s-":
        format_vinyl = "test press"
    else :
        format_vinyl = format_vinyl_url

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
                
                add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)

    return results


async def scrap_onlyrootsreggae(client, url):

    print('url: ', url)
    results = []
    # reggea Shop name
    name_shop = "onlyroots-reggae.com"

    # parse HTML 
    html = await get_url(client, url)

    # retrieve all tags article with class=product-miniature
    lst_articles = html.css("article.product-miniature")

    async with httpx.AsyncClient(timeout=None) as client2:
        for vinyl in lst_articles:
            vinyl_link = vinyl.css_first("link").attributes.get("href")
            
            # open url link_vinyl for retrieve mp3 link 
            html_page_vinyl = await get_url(client2, vinyl_link)

            if html_page_vinyl.css_matches('source'):
                vinyl_title = html_page_vinyl.css_first("h1.page-heading").text() 
                vinyl_image = html_page_vinyl.css_first("img.img-fluid").attributes.get("src")
                format_vinyl = vinyl_title.split(" ")[0].replace(')', "").replace('(', "").replace('"', "")

                # retrieve all mp3
                lst_mp3 = html_page_vinyl.css('source')

                for mp3 in lst_mp3:
                    mp3_title = mp3.attributes.get("title")
                    mp3_link = "https://www.onlyroots-reggae.com" + mp3.attributes.get("src")

                    add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)

    return results


def scrap_controltower(url):

    print('url: ', url)
    results = []
    # reggea Shop name
    name_shop = "controltower.fr"

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
            
            vinyl_title = html_page_vinyl.css_first('h1').text()
            vinyl_image = html_page_vinyl.css_first('img#bigpic').attributes.get("src")
            format_vinyl = html_page_vinyl.css_first("option").text().replace(')', "").replace('(', "").replace('"', "")

            # retrieve all mp3
            lst_mp3 = html_page_vinyl.css('source')

            for mp3 in lst_mp3:
                mp3_title = mp3.attributes.get("title")
                mp3_link = mp3.attributes.get("src")
                
                add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)

    return results


async def scrap_reggaefever(client, url):
    print('url: ', url)
    results = []
    date_ann = ['2017','2018','2019','2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    # if function call by customSearch don't skip the firsts articles
    nb_art_no_take = 0 if "generic" in url else 2
    # reggea Shop name
    name_shop = "reggaefever.ch"

    # parse HTML 
    html = await get_url(client, url)

    # retrieve all tags tr
    lst_articles = html.css("tr")

    for item in lst_articles[nb_art_no_take:]:
        if item.text().lstrip()[:4] not in date_ann:
            if item.css_matches('td.articleFormat'):
                format_vinyl = item.css_first('td.articleFormat').text()

            if item.css_matches("td.artist"):
                vinyl_title = item.css_first("td.artist").text() + ' - ' + item.css_first("td.title").text()

            if item.css_matches("img.articleIcon"):
                vinyl_image = item.css_first("img.articleIcon").attributes.get("src")

            if item.css_matches("a"):
                vinyl_link = 'https://www.reggaefever.ch/' + item.css_first("a").attributes.get("href")

            if item.css_matches("td.title"):
                mp3_title = item.css_first("td.title").text()
            else:
                mp3_title= "version"

            if item.css_matches('a[target=rfplayer]'):
                mp3_link = item.css_first('a[target=rfplayer]').attributes.get('href')

                add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)

    return results


async def scrap_deeprootsreggae(client, url):
    print('url: ', url)
    results = []

    # reggea Shop name
    name_shop = "deeprootsreggaeshop.com"

    # parse HTML 
    html = await get_url(client, url)

    # retrieve all tags tr
    lst_articles = html.css("a.ProductName")

    async with httpx.AsyncClient(timeout=None) as client2:
        for vinyl in lst_articles:

            vinyl_link = "http://www.deeprootsreggaeshop.com/epages/300210.sf/en_GB/" + vinyl.attributes.get('href')

            # open url link_vinyl for retrieve mp3 link 
            html_page_vinyl = await get_url(client2, vinyl_link)
            
            description = html_page_vinyl.css_first('div.description')

            # verif if mp3 exists on this page 
            if description:
                if description.css_matches('a'):
                    vinyl_title = html_page_vinyl.css_first('h1').text()
                    div_img = html_page_vinyl.css_first('div.ProductImage')
                    vinyl_image = "http://www.deeprootsreggaeshop.com" + div_img.css_first('img').attributes.get('src')

                    p_format = description.css('p')

                    if '7"' in p_format[-1].text():
                        format_vinyl = "7"
                    elif '10"' in p_format[-1].text():
                        format_vinyl = "10"
                    elif '12"' in p_format[-1].text():
                        format_vinyl = "12"
                    else :
                        format_vinyl = "lp"

                    lst_mp3 = description.css('a')

                    for mp3 in lst_mp3:
                        mp3_title = vinyl_title
                        mp3_link = mp3.attributes.get('href')

                        add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)

    return results


def scrap_rastavibes(url):
    print('url: ', url)
    results = []

    # reggea Shop name
    name_shop = "rastavibes.net"
    
    #object of ChromeOptions
    options = webdriver.ChromeOptions()
    #setting headless parameter
    options.headless = True

    service = Service(executable_path="D:/DEV/VinylsDubScrap_NewVersion/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1700, 1080)
    

    for url_page in url:
        
        driver.get(url_page)

        # retreive div main with vinyls 
        div_main = driver.find_element(By.ID, "homecontent")
        
        # retreive all element with icone sound for load mp3 source 
        lst_vinyls = div_main.find_elements(By.CSS_SELECTOR, ".sprite-sound")

        # range and click on all element for display mp3 source
        for x in lst_vinyls:
            x.click()
            time.sleep(0.5)

            # retrieve div with vinyl with mp3
            div_vinyl = div_main.find_element(By.ID, "player")

            # format 
            format_vinyl = div_vinyl.find_element(By.CSS_SELECTOR, ".format").text.replace('"', '')

            # link vinyl page
            div_link_vinyl = div_vinyl.find_element(By.CLASS_NAME, "ref")
            vinyl_link = div_link_vinyl.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # title 
            div_title = div_vinyl.find_element(By.TAG_NAME, "p")
            text_title = div_title.text.split('\n')
            vinyl_title = " - ".join(text_title[:-1]).replace("Label : ", "").replace("Artiste : ", "").replace("Titre : ", "")
            
            # image 
            vinyl_image = div_vinyl.find_element(By.CLASS_NAME, "cover").get_attribute("src")
            
            # mp3
            # click on btn play for display mp3 link
            btn_play = div_vinyl.find_element(By.CSS_SELECTOR, ".ui-button")
            btn_play.click() #play 
            btn_play.click() #pause
            div_mp3 = div_vinyl.find_element(By.TAG_NAME, "audio")
            lst_mp3 = div_mp3.find_elements(By.TAG_NAME, "a")
            for mp3 in lst_mp3:
                mp3_title = text_title[2]
                mp3_link = mp3.get_attribute('href')

                add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)

    driver.close()
    return results


async def scrap_pataterecords(client, url):
    print('url: ', url)
    results = []

    # reggea Shop name
    name_shop = "patate-records.com"

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

                if '7' in format_vinyl:
                    format_vinyl = "7"
                elif 'LP' in format_vinyl:
                    format_vinyl = "lp"
                elif len(lst_mp3) < 5:
                    format_vinyl = "10"
                else:
                    format_vinyl = "12"

                
                for mp3 in lst_mp3[:-1]:
                    if mp3.css_matches("source"):
                        mp3_title = mp3.text().split('\n')[-1]
                        mp3_link = mp3.css_first("source").attributes.get("src")

                        add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)

    return results


async def scrap_toolboxrecords(client, url):
    print('url: ', url)
    results = []

    # reggea Shop name
    name_shop = "toolboxrecords.com"

    # parse HTML 
    html = await get_url(client, url)

    # retrieve all tags article with class=product-miniature
    lst_articles = html.css("div.product-cell-thumb")

    # async with httpx.AsyncClient(timeout=None) as client2:
    for vinyl in lst_articles:

        if vinyl.css_matches("ul.product-track-listing"):

            vinyl_image = vinyl.css_first("img").attributes.get("src")
            vinyl_link = vinyl.css_first("a").attributes.get("href")
            vinyl_title = vinyl.css_first("span.product-name").text() + ' - ' + vinyl.css_first("div.product-infos-details").css_first('li').text()


            format_vinyl = vinyl.css_first("div.product-infos-details").css_first('ul').text()            
            if "7''" in format_vinyl:
                format_vinyl = "7"
            elif 'LP' in format_vinyl or 'CD' in format_vinyl:
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
                mp3_link = "https://www.toolboxrecords.com/public/mp3/" + mp3.css_first("div.track-title").attributes.get("rel")
            
                add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)
            
    return results


async def scrap_lionvibes(client, url):
    print('url: ', url)
    results = []

    # reggea Shop name
    name_shop = "lionvibes.com"

    # parse HTML 
    html = await get_url(client, url)

    # retrieve all tags article with class=album-block
    lst_articles = html.css("div.album-block")

    for vinyl in lst_articles:
        vinyl_image = "https://shop.lionvibes.com" + vinyl.css_first("img").attributes.get("src")
        div_link =  vinyl.css("a")
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

                add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link)

    return results


async def scrap_reggaemuseum(client, url):
    print('url: ', url)
    results = []

    # reggea Shop name
    name_shop = "reggae-museum.com"

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
                
                if '7' in vinyl_title:
                    format_vinyl = "7"
                elif '10' in vinyl_title:
                    format_vinyl = "10"
                elif '12' in vinyl_title:
                    format_vinyl = "12"
                else:
                    format_vinyl = "lp"

                if lst_mp3[-2].css_matches("a"):
                    track_A = lst_mp3[1].css("td")[-1].text().lstrip().rstrip()
                    link_mp3_A = lst_mp3[-2].css_first("a").attributes.get("href")

                    add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, track_A, link_mp3_A)


                if lst_mp3[-1].css_matches("a"):
                    track_B = lst_mp3[4].css("td")[-1].text().lstrip().rstrip()
                    link_mp3_B = lst_mp3[-1].css_first("a").attributes.get("href")

                    add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, track_B, link_mp3_B)
            
    return results


# async def scrap_reggaecouk(client, url):
#     return True

# async def scrap_unearthedsounds(client, url):
#     print('url: ', url)
#     results = []

#     # reggea Shop name
#     name_shop = "unearthedsounds"

#     # parse HTML 
#     html = await get_url(client, url)

#     # retireve all articles
#     lst_articles = html.css('div.product-tile')

#     async with httpx.AsyncClient(timeout=None) as client2:
#         for item in lst_articles:
#             if item.css_matches('span.play-button-label'):
                
#                 vinyl_link = "https://www.unearthedsounds.co.uk/" + item.css_first('a').attributes.get('href')
#                 vinyl_title = ' - '.join(f'{x.text()}' for x in item.css('a.undecorated-link'))
                
#                 format_vinyl = item.css_first('li.format ').text().lstrip().rstrip()
#                 if format_vinyl == "Download":
#                     format_vinyl = "LP"

#                 # open url link_vinyl for retrieve mp3 link 
#                 html_page_vinyl = await get_url(client2, vinyl_link)

#                 vinyl_image = html_page_vinyl.css_first('[itemprop=image]').attributes.get('src')

#                 lst_mp3 = html_page_vinyl.css('audio.jp_audio_0')
#                 print('lst_mp3', lst_mp3)

#                 print('vinyl_title', vinyl_title)
#                 print('vinyl_link', vinyl_link)
#                 print('format_vinyl', format_vinyl)
#                 print('vinyl_image', vinyl_image)
#                 break


# Il faut le faire avec Selenium car le mp3 link s'affiche quelques secondes après le load de la page 
# async def scrap_reggaeduborg(client, url):

#     print('url: ', url)
#     results = []

#     # reggea Shop name
#     name_shop = "reggaeduborg"

#     # parse HTML 
#     html = await get_url(client, url)
    
#     # retrieve all articles
#     lst_articles = html.css("article.product-miniature")

#     async with httpx.AsyncClient(timeout=None) as client2:
#         for vinyl in lst_articles:
#             vinyl_image = vinyl.css_first("img").attributes.get("src")
#             vinyl_link = vinyl.css_first("a").attributes.get("href")

#             # open url link_vinyl for retrieve mp3 link 
#             html_page_vinyl = await get_url(client2, vinyl_link)
#             vinyl_title = html_page_vinyl.css_first("h1.h1").text()

#             print(html_page_vinyl.html)

#             lst_mp3 = html_page_vinyl.css_first("div#jquery_jplayer_1")

#             print("vinyl_title", vinyl_title)
#             print("vinyl_image", vinyl_image)
#             print("vinyl_link", vinyl_link)
#             print("lst_mp3", lst_mp3)

#             break
#     return True




async def get_url(client, url):
    # get acces to url
    res = await client.get(url)
    # parse HTML 
    return HTMLParser(res.text)


def add_to_class(results, name_shop, format_vinyl, vinyl_title, vinyl_image, vinyl_link, mp3_title, mp3_link):

    # create new dataframe with new row 
    new_item = Vinyl(name_shop=name_shop,
    format_vinyl=format_vinyl,
    vinyl_title=vinyl_title,
    vinyl_image=vinyl_image,
    vinyl_link=vinyl_link,
    mp3_title=mp3_title,
    mp3_link=mp3_link)
    
    # add the new item
    results.append(asdict(new_item))


def to_csv(list_vinyls):
    print('open CSV')

    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open('out.csv', 'a', encoding='utf-8') as f:

        for item in list_vinyls:
            # Pass this file object to csv.writer()
            writer = csv.DictWriter(f, fieldnames=["name_shop","format_vinyl","vinyl_title","vinyl_image","vinyl_link","mp3_title","mp3_link"])
        
            # Pass the list as an argument into
            writer.writerows(item)

        # Close the file object
        f.close()


async def main():

    # # ---------------------------------------------------------------------------------
    # # JAH WAGGYS RECORDS
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        print('start scrap_jahwaggysrecords')
        tasks.extend(scrap_jahwaggysrecords(client, url) for url in urls_jahwaggys)
        lst_jahwaggysrecords = await asyncio.gather(*tasks)
    # insert in CSV
    to_csv(lst_jahwaggysrecords)


    # ---------------------------------------------------------------------------------
    # CONTROL TOWER RECORDS
    # insert in CSV
    print('start scrap_controltower')
    to_csv([scrap_controltower(url_controltower)])


    # ---------------------------------------------------------------------------------
    # ONLY ROOTS REGGAE 
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        print('start scrap_onlyrootsreggae')
        tasks.extend(scrap_onlyrootsreggae(client, url) for url in urls_onlyrootsreggae)
        lst_onlyrootsreggae = await asyncio.gather(*tasks)
    # insert in CSV
    to_csv(lst_onlyrootsreggae)



    # # ---------------------------------------------------------------------------------
    # # REGGAE FEVER
    # tasks = []
    # async with httpx.AsyncClient(timeout=None) as client:
    #     print('start scrap_reggaefever')
    #     tasks.extend(scrap_reggaefever(client, url) for url in urls_reggaefever)
    #     lst_reggaefever = await asyncio.gather(*tasks)
    # # insert in CSV
    # to_csv(lst_reggaefever)



    # ---------------------------------------------------------------------------------
    # DEEP ROOTS REGGAE
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        print('start scrap_deeprootsreggae')
        tasks.extend(scrap_deeprootsreggae(client, url) for url in urls_deeprootsreggae)
        lst_deeprootsreggae = await asyncio.gather(*tasks)
    # insert in CSV
    to_csv(lst_deeprootsreggae)


    # ---------------------------------------------------------------------------------
    # RASTAVIBES
    print('start scrap_rastavibes')
    lst_rastavibes = [scrap_rastavibes(urls_rastavibes)]
    # insert in CSV
    to_csv(lst_rastavibes)


    # ---------------------------------------------------------------------------------
    # PATATE RECORDS
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        print('start scrap_pataterecords')
        tasks.extend(scrap_pataterecords(client, url) for url in urls_pataterecords)
        lst_pataterecords = await asyncio.gather(*tasks)
    # # insert in CSV
    to_csv(lst_pataterecords)


    # # ---------------------------------------------------------------------------------
    # TOOLBOX RECORDS
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        print('start scrap_toolboxrecords')
        tasks.extend(scrap_toolboxrecords(client, url) for url in urls_toolboxrecords)
        lst_toolboxrecords = await asyncio.gather(*tasks)
    # # insert in CSV
    to_csv(lst_toolboxrecords)


    # ---------------------------------------------------------------------------------
    # LION VIBES
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        print('start scrap_lionvibes')
        tasks.extend(scrap_lionvibes(client, url) for url in urls_lionvibes)
        lst_lionvibes = await asyncio.gather(*tasks)
    # insert in CSV
    to_csv(lst_lionvibes)


    # # ---------------------------------------------------------------------------------
    # # REGGAE MUSEUM 
    tasks = []
    async with httpx.AsyncClient(timeout=None) as client:
        print('start scrap_reggaemuseum')
        tasks.extend(scrap_reggaemuseum(client, url) for url in urls_reggaemuseum)
        lst_reggaemuseum = await asyncio.gather(*tasks)
    # insert in CSV
    to_csv(lst_reggaemuseum)




    # # ---------------------------------------------------------------------------------
    # # UNEARTHED SOUNDS NE MARCHE PAS , on peux pas recup les mp3
    # tasks = []
    # async with httpx.AsyncClient(timeout=None) as client:
    #     tasks.extend(scrap_unearthedsounds(client, url) for url in urls_unearthedsounds)
    #     lst_unearthedsounds = await asyncio.gather(*tasks)
    # # insert in CSV
    # # to_csv(lst_unearthedsounds)



    # # ---------------------------------------------------------------------------------
    # # REGGAE DUB .ORG - A FAIRE AVEC SELENIUM 
    # tasks = []
    # async with httpx.AsyncClient(timeout=None) as client:
    #     tasks.extend(scrap_reggaeduborg(client, url) for url in urls_reggaeduborg)
    #     lst_reggaeduborg = await asyncio.gather(*tasks)
    # # insert in CSV
    # to_csv(lst_deeprootsreggae)




# main()
if __name__ == '__main__':
    asyncio.run(main())