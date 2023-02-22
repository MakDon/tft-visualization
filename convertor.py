import json
import requests
import os
from urllib.parse import urlparse

chess = json.load(open("./json/chess.json"))
job = json.load(open("./json/job.json"))
race = json.load(open("./json/race.json"))
trait = json.load(open("./json/trait.json"))
neo_graph = {}

def download_img(data_set):
    for k, data in data_set["data"].items():
        url = data["picture"]
        parsed_url = urlparse(url)
        response = requests.get(url)
        open("./img/" + os.path.basename(parsed_url.path), "wb").write(response.content)

def download_all_img():
    download_img(chess)
    download_img(job)
    download_img(race)
    download_img(trait)

def parse_chess(all_chess):
    pass

if __name__ == "__main__":
    download_all_img()
