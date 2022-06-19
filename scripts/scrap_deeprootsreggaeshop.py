import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from mutagen.mp3 import MP3
import time
import json


# sourcery skip: use-assigned-variable
def scrap_deeprootsreggaeshop(list_url):

    def collect_mp3(url_page):
        # open url page Vinyl for collect url mp3
        data_page_vinyl = requests.get(url_page).content
        soup_2 = BeautifulSoup(data_page_vinyl, "lxml")

        # collect all source mp3
        list_source = soup_2.find_all("div", {"class": "description"})

        for source in list_source:
            mp3_title_vinyl = source.find("p").text
            mp3_url_vinyl = source.find("a")['href']
            if mp3_url_vinyl[-7:] == 'mp3.mp3':
                mp3_url_vinyl = mp3_url_vinyl[:-4]

            # colect duration with url mp3 of song
            filename, header = urlretrieve(mp3_url_vinyl)
            audio = MP3(filename)
            mp3_duration = time.strftime(
                "%H:%M:%S", time.gmtime(audio.info.length))[3:]

            list_data_vinyl.append({'titre': title_vinyl, 'url': url_vinyl, 'img': img_vinyl,
                                    'songTitle': mp3_title_vinyl, 'songUrl': mp3_url_vinyl, 'songDuration': mp3_duration})

    sauv_url = "http://www.deeprootsreggaeshop.com/epages/300210.sf/en_GB/?ObjectPath=/Shops/300210/Categories/%22nouvelles%20entrees%22"
    i = 0
    for url in list_url:

        list_data_vinyl = []
        print('url: ', url)
        data_url_principal = requests.get(url).content
        soup = BeautifulSoup(data_url_principal, "lxml")

        list_div = soup.find_all('div', {"class": "HotDeal"})
        if len(list_div) > 0:
            for vinyl in list_div:

                # IMAGE
                img_vinyl = vinyl.find(
                    "img", {"class": "ProductHotDealImage"})
                img_vinyl = 'http://www.deeprootsreggaeshop.com' + \
                    img_vinyl['src']

                # Title Vinyl
                title_vinyl = vinyl.find("a", {"class": "ProductName"})
                title_vinyl = title_vinyl['title']

                # URL vinyl
                url_vinyl = vinyl.find("a", {"class": "ProductName"})
                url_vinyl = 'http://www.deeprootsreggaeshop.com/epages/300210.sf/en_GB/' + \
                    url_vinyl['href']

                collect_mp3(url_vinyl)
        else:
            list_div = soup.find_all('div', {"class": "InfoArea"})
            for vinyl in list_div:

                # IMAGE
                img_div = vinyl.find(
                    "img", {"class": "ProductSmallImage"})
                img_vinyl = 'http://www.deeprootsreggaeshop.com' + \
                    img_div['src']

                # Title Vinyl
                title_vinyl = img_div['alt']

                # URL vinyl
                url_div = vinyl.find("td", {"class": "AlignTop"})
                url_vinyl = url_div.find("a")
                url_vinyl = 'http://www.deeprootsreggaeshop.com/epages/300210.sf/en_GB/' + \
                    url_vinyl['href']

                # call function for collect all mp3
                collect_mp3(url_vinyl)

        # choose which file use
        if url == sauv_url:
            file_json_path = 'json\outputDeepRootsReggaeShop.json'
        else:
            file_json_path = 'json\outputCustomSearch.json'

        print('file_json_path: ', file_json_path)
        with open(file_json_path, 'w') as f:
            # delete data
            f.truncate

            # all in one line
            f.write(json.dumps(list_data_vinyl, indent=4))
            i = i + 1
