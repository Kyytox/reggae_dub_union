from queue import Empty
from numpy import empty
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
import time
import json
import os


def scrap_reggaeDub(list_url):

    sauv_url = "https://www.reggaedub.org/fr/14-7"
    i = 0

    for url in list_url:

        list_data_vinyl = []
        print('url: ', url)
        data_url_principal = requests.get(url).content
        soup = BeautifulSoup(data_url_principal, "lxml")

        list_vinyls = soup.find_all('a', class_='product-thumbnail')

        for vinyl in list_vinyls:

            # url vinyl
            url_vinyl = vinyl['href']
            print('url_vinyl: ', url_vinyl)

            # img vinyl
            img_vinyl = vinyl.find('img')['src']
            print('img_vinyl: ', img_vinyl)

            # open url page Vinyl for collect url mp3
            data_page_vinyl = requests.get(url_vinyl).content
            soup_2 = BeautifulSoup(data_page_vinyl, "html")

            div_content_vinyl = soup_2.find('div', class_='listing')
            # print('div_content_vinyl: ', div_content_vinyl)
            div_content_vinyl_2 = soup_2.find_all(
                'div', {"class": "center"})
            print('div_content_vinyl_2: ', div_content_vinyl_2)
            break

            # title Vinyl
            title_vinyl = div_content_vinyl.find('h1').text

            # mp3 Vinyl
            mp3_vinyl_list = div_content_vinyl.find(
                'div', class_='traclist_detail')

            if mp3_vinyl_list != None:
                for source in mp3_vinyl_list:
                    # Title mp3
                    if 'audio' in source.text:
                        list_text = source.text.split('audio')
                        mp3_title_vinyl = list_text[1]
                        mp3_title_vinyl = mp3_title_vinyl.replace("\n", "")
                    else:
                        mp3_title_vinyl = list_text[0]

                    # URL mp3
                    if len(source('source')) != 0:
                        mp3_url_vinyl = source.find('source')['src']
                    else:
                        continue

                    print('mp3_url_vinyl : ', mp3_url_vinyl)
                    # colect duration with url mp3 of song
                    filename, header = urlretrieve(mp3_url_vinyl)
                    print('filename : ', filename)
                    print('os.path.getsize', os.path.getsize(filename))
                    if os.path.getsize(filename) < 50000:
                        continue

                    audio = MP3(filename)
                    mp3_duration = time.strftime(
                        "%H:%M:%S", time.gmtime(audio.info.length))[3:]
                    os.remove(filename)

                    list_data_vinyl.append(
                        {'titre': title_vinyl, 'url': url_vinyl, 'img': img_vinyl, 'songTitle': mp3_title_vinyl, 'songUrl': mp3_url_vinyl, 'songDuration': mp3_duration})

        break
        # choose which file use
        if i == 0:
            file_json_path = '../json/outputRastaVibes7.json' if url == sauv_url else '../json/outputCustomSearch.json'
        elif i == 1:
            file_json_path = '../json/outputRastaVibes1012.json'
        elif i == 2:
            file_json_path = '../json/outputRastaVibesLP.json'

        print('os.getcwd() :', os.getcwd())
        print('file_json_path: ', file_json_path)
        with open(file_json_path, 'w') as f:
            # delete data
            f.truncate

            # all in one line
            f.write(json.dumps(list_data_vinyl, indent=4))
            i = i + 1
