import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
import time
import json


def scrap_reggaefever(list_url):  # sourcery skip: low-code-quality

    i = 0
    for url in list_url:

        list_data_vinyl = []
        print('url: ', url)
        data_url_principal = requests.get(url).content
        soup = BeautifulSoup(data_url_principal, "lxml")

        list_tr = soup.find_all('tr')[1:]
        # del list_tr[:1]

        for vinyl in list_tr:
            # we don't take tr with date
            if vinyl.text.lstrip()[:4] != '2022' and '2023':

                # IMAGE
                if vinyl.find("td", {"class": "articleListInfo"}) != None:
                    data_img = vinyl.find("td", {"class": "articleListInfo"})
                    img_vinyl = data_img.find("img")['src']

                # Title Vinyl
                # if Title = null we take val of the previous tr
                if vinyl.find("td", {"class": "artist"}).text != '':
                    title_vinyl = vinyl.find("td", {"class": "artist"}).text

                # URL and TITLE
                data_title = vinyl.find("td", {"class": "title"})
                url_vinyl = "https://www.reggaefever.ch/" + \
                    data_title.find("a")['href']
                mp3_title_vinyl = data_title.text

                # MP3
                # if len of data_mp3 = 1 = no data so on collect the previous url mp3
                if len(vinyl.find("td", {"class": "sample"})) != 1:
                    data_mp3 = vinyl.find("td", {"class": "sample"})
                    mp3_url_vinyl = data_mp3.find("a")['href']

                # colect duration with url mp3 of song
                filename, header = urlretrieve(mp3_url_vinyl)
                audio = MP3(filename)
                mp3_duration = time.strftime(
                    "%H:%M:%S", time.gmtime(audio.info.length))[3:]

                list_data_vinyl.append(
                    {'titre': title_vinyl, 'url': url_vinyl, 'img': img_vinyl, 'songTitle': mp3_title_vinyl, 'songUrl': mp3_url_vinyl, 'songDuration': mp3_duration})

        # choose which file use
        if i == 0:
            file_json_path = 'json\outputReggaeFever7.json' if url == sauv_url else 'json\outputCustomSearch.json'
        elif i == 1:
            file_json_path = 'json\outputReggaeFever10.json'
        elif i == 2:
            file_json_path = 'json\outputReggaeFever12.json'

        print('file_json_path: ', file_json_path)
        with open(file_json_path, 'w') as f:
            # delete data
            f.truncate

            # all in one line
            f.write(json.dumps(list_data_vinyl, indent=4))
            i = i + 1


# initialisation url_vinyl
# call function scraping ReggaeFever
sauv_url = "https://www.reggaefever.ch/articleList?format=7&special=reissues&newRel=0&sort=relDate_riddim"
list_url = ["https://www.reggaefever.ch/articleList?format=7&special=reissues&newRel=0&sort=relDate_riddim",
            "https://www.reggaefever.ch/articleList?format=10&newRel=0&sort=relDate_riddim", "https://www.reggaefever.ch/articleList?format=12&newRel=0&sort=relDate_riddim&noStyle=Hip+Hop&noStyle=R%2BB"]
# scrap_reggaefever(list_url)
