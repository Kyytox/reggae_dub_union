import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
import time
import json
import os


def scrap_jahwaggys(list_url):

    sauv_url = "https://jahwaggysrecords.com/fr/5-brand-new-7-vinyl-selection"
    i = 0

    for url in list_url:

        list_data_vinyl = []
        print('url: ', url)
        data_url_principal = requests.get(url).content
        soup = BeautifulSoup(data_url_principal, "lxml")

        list_vinyls = soup.find_all('h3', class_='h3 product-title')

        del list_vinyls[:14]

        for vinyl in list_vinyls:

            # url vinyl
            url_vinyl = vinyl.find('a')['href']

            # title Vinyl
            title_vinyl = vinyl.find('a').text
            title_vinyl = title_vinyl.split('"')[0]

            data_vinyl = requests.get(vinyl.find('a')['href']).content
            soup_vinyl_page = BeautifulSoup(data_vinyl, "lxml")

            img_vinyl_list = soup_vinyl_page.find_all(
                'img', class_="js-qv-product-cover")

            for img in img_vinyl_list:
                # img Vinyl
                img_vinyl = img['src']

            # mp3 Vinyl
            mp3_vinyl_list = soup_vinyl_page.find_all('a', class_="sm2_button")

            for mp3 in mp3_vinyl_list:
                mp3_url_vinyl = "https://jahwaggysrecords.com" + mp3['href']

                # colect duration with url mp3 of song
                filename, header = urlretrieve(mp3_url_vinyl)
                audio = MP3(filename)
                mp3_duration = time.strftime(
                    "%H:%M:%S", time.gmtime(audio.info.length))[3:]
                os.remove(filename)

                mp3_title_vinyl = mp3['title']
                list_data_vinyl.append(
                    {'titre': title_vinyl, 'url': url_vinyl, 'img': img_vinyl, 'songTitle': mp3_title_vinyl, 'songUrl': mp3_url_vinyl, 'songDuration': mp3_duration})

        # choose which file use
        if i == 0:
            file_json_path = 'json\outputJahWaggys7.json' if url == sauv_url else 'json\outputCustomSearch.json'
        elif i == 1:
            file_json_path = 'json\outputJahWaggys10.json'
        elif i == 2:
            file_json_path = 'json\outputJahWaggys12.json'

        print('file_json_path: ', file_json_path)
        with open(file_json_path, 'w') as f:
            # delete data
            f.truncate

            # all in one line
            f.write(json.dumps(list_data_vinyl, indent=4))
            i = i + 1
