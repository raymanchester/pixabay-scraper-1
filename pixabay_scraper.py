from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import os
from datetime import datetime

project_wd = os.getcwd()


def start_search(phrase):
    dir_name = "search_" + phrase + "_" + str(datetime.now().strftime("%d-%b-%Y"))

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    os.chdir(dir_name)

    r = requests.get("https://pixabay.com/pl/images/search/" + phrase)

    soup = BeautifulSoup(r.text, "html.parser")
    urls = soup.findAll("img")

    for url in urls:
        try:
            img_url = requests.get(url.attrs["src"])
            title = url.attrs["src"].split("/")[-1]
            image = Image.open(BytesIO(img_url.content))
            image.save(title, image.format)
        except requests.exceptions.MissingSchema:
            break

    global project_wd
    os.chdir(project_wd)


search_list = ["database", "computer", "laptop", "work"]

for item in search_list:
    start_search(item)
