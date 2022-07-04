import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
import time
import json
import os


def scrap_unearthedsounds(list_url):

    sauv_url = "https://www.unearthedsounds.co.uk/collections/a-reggae-dub?sort_by=created-descending"
    i = 0
    txt_del = "{width}"
    for url in list_url:

        list_data_vinyl = []

        print('url: ', url)
        data_url_principal = requests.get(url).content
        soup = BeautifulSoup(data_url_principal, "lxml")

        list_div = soup.find_all("a", {"class": "grid-product__link"})

        for vinyl in list_div:

            # IMAGE
            img_vinyl = vinyl.find(
                "img", {"class": "grid-image-dim"})['data-src']
            img_vinyl = "https:" + img_vinyl.replace(txt_del, '360')

            # Title Vinyl
            title_vinyl = vinyl.find("img", {"class": "grid-image-dim"})['alt']

            # URL vinyl
            url_vinyl = "https://www.unearthedsounds.co.uk" + vinyl['href']

            # open url page Vinyl for collect url mp3
            data_page_vinyl = requests.get(url_vinyl).content
            soup_2 = BeautifulSoup(data_page_vinyl, "lxml")

            # collect all source mp3
            list_source = soup_2.find_all(
                "div", {"class": "product-single__description"})

            for source in list_source:
                list_p = source.find_all("p")[1:]
                # print('list_p: ', list_p)
                for p in list_p:
                    if p.text:
                        mp3_title_vinyl = p.text
                    else:
                        list_audio = p.find_all('audio')
                        for url in list_audio:
                            mp3_url_vinyl = url['src']

                            # colect duration with url mp3 of song
                            filename, header = urlretrieve(mp3_url_vinyl)
                            audio = MP3(filename)
                            mp3_duration = time.strftime(
                                "%H:%M:%S", time.gmtime(audio.info.length))[3:]
                            os.remove(filename)

                            list_data_vinyl.append({'titre': title_vinyl, 'url': url_vinyl, 'img': img_vinyl,
                                                    'songTitle': mp3_title_vinyl, 'songUrl': mp3_url_vinyl, 'songDuration': mp3_duration})

        # choose which file use
        file_json_path = 'json\outputUnearthedSounds.json' if url == sauv_url else 'json\outputCustomSearch.json'

        print('file_json_path: ', file_json_path)
        with open(file_json_path, 'w') as f:
            # delete data
            f.truncate

            # all in one line
            f.write(json.dumps(list_data_vinyl, indent=4))
            i = i + 1
