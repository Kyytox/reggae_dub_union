import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
import time
import json
import os


def scrap_controltowerrecords(list_url):

    sauv_url = "https://controltower.fr/fr/"
    i = 0
    for url in list_url:

        list_data_vinyl = []
        print('url: ', url)
        data_url_principal = requests.get(url).content
        soup = BeautifulSoup(data_url_principal, "lxml")

        list_div = soup.find_all(
            'div', {"class": "product-container"}, limit=30)

        for vinyl in list_div:

            # IMAGE
            img_vinyl = vinyl.find("img", {"class": "lazy"})['data-src']

            # Title Vinyl
            # if Title Vinyl = null we take val of the previous tr
            title_vinyl = vinyl.find(
                "a", {"class": "product_img_link"})['title']

            # URL vinyl
            url_vinyl = vinyl.find("a", {"class": "product_img_link"})['href']

            # open url page Vinyl for collect url mp3
            data_page_vinyl = requests.get(url_vinyl).content
            soup_2 = BeautifulSoup(data_page_vinyl, "lxml")

            # collect all source mp3
            list_source = soup_2.find_all("source")

            for source in list_source:
                mp3_title_vinyl = source['title']
                if '%' in mp3_title_vinyl:
                    continue

                mp3_url_vinyl = source['src']

                # colect duration with url mp3 of song
                filename, header = urlretrieve(mp3_url_vinyl)
                audio = MP3(filename)
                mp3_duration = time.strftime(
                    "%H:%M:%S", time.gmtime(audio.info.length))[3:]
                os.remove(filename)

                list_data_vinyl.append(
                    {'titre': title_vinyl, 'url': url_vinyl, 'img': img_vinyl, 'songTitle': mp3_title_vinyl, 'songUrl': mp3_url_vinyl, 'songDuration': mp3_duration})

        # choose which file use
        if url == sauv_url:
            file_json_path = 'json\outputControlTowerRecords.json'
        else:
            file_json_path = 'json\outputCustomSearch.json'

        print('file_json_path: ', file_json_path)
        with open(file_json_path, 'w') as f:
            # delete data
            f.truncate

            # all in one line
            f.write(json.dumps(list_data_vinyl, indent=4))
            i = i + 1
