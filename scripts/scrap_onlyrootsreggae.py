import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
import time
import json
import os


# sourcery skip: use-assigned-variable
def scrap_onlyrootsreggae(list_url):

    sauv_url = "https://www.onlyroots-reggae.com/fr/21-singles-7-45t/s-1/nouveautes-oui?order=product.date_upd.desc"
    i = 0
    for url in list_url:

        list_data_vinyl = []
        print('url: ', url)
        data_url_principal = requests.get(url).content
        soup = BeautifulSoup(data_url_principal, "lxml")

        list_div = soup.find_all('article', {"class": "product-miniature"})
        # print('list_div: ', list_div)

        for vinyl in list_div:
            # URL vinyl
            url_vinyl = vinyl.find(
                "a", {"class": "product-cover-link"})['href']

            # Title Vinyl
            title_vinyl = vinyl.find("img")['alt']

            # IMAGE
            img_vinyl = vinyl.find("img")['src']

            # open url page Vinyl for collect url mp3
            data_page_vinyl = requests.get(url_vinyl).content
            soup_2 = BeautifulSoup(data_page_vinyl, "lxml")

            # collect all source mp3
            list_soucre = soup_2.find_all("source")

            for source in list_soucre:
                mp3_title_vinyl = source['title']
                mp3_url_vinyl = "https://www.onlyroots-reggae.com" + \
                    source['src']

                # colect duration with url mp3 of song
                filename, header = urlretrieve(mp3_url_vinyl)
                audio = MP3(filename)
                mp3_duration = time.strftime(
                    "%H:%M:%S", time.gmtime(audio.info.length))[3:]
                os.remove(filename)

                list_data_vinyl.append({'titre': title_vinyl, 'url': url_vinyl, 'img': img_vinyl,
                                        'songTitle': mp3_title_vinyl, 'songUrl': mp3_url_vinyl, 'songDuration': mp3_duration})

        # choose which file use
        if i == 0:
            file_json_path = 'json\outputOnlyRootsReggae7.json' if url == sauv_url else 'json\outputCustomSearch.json'
        elif i == 1:
            file_json_path = 'json\outputOnlyRootsReggae1012.json'
        elif i == 2:
            file_json_path = 'json\outputOnlyRootsReggaeLP.json'

        print('file_json_path: ', file_json_path)
        with open(file_json_path, 'w') as f:
            # delete data
            f.truncate

            # all in one line
            f.write(json.dumps(list_data_vinyl, indent=4))
            i = i + 1
