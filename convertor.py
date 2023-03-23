import json
import requests
import os
from urllib.parse import urlparse

chess = json.load(open("./json/chess.json"))
job = json.load(open("./json/job.json"))
race = json.load(open("./json/race.json"))
trait = json.load(open("./json/trait.json"))
neo_graph = {
    "results": [{
        "columns": ["user", "entity"],
        "data":[{
            "graph": {
                "nodes": [],
                "relationships": []
            }
        }]
    }],
    "errors": []
}

def download_img(data_set):
    for k, data in data_set["data"].items():
        url = data["picture"]
        parsed_url = urlparse(url)
        response = requests.get(url)
        open("./img/" + os.path.basename(parsed_url.path), "wb").write(response.content)
        print("Download " + data["name"] + "Done")

def download_all_img():
    download_img(chess)
    download_img(job)
    download_img(race)
    download_img(trait)


def convert_to_neo4j_data():
    parse_chess()
    parse_job()
    parse_race()
    parse_trait()
    with open("./json/neo4jData.json", "w") as fp:
        json.dump(neo_graph, fp)
    with open("./neo4jd3/docs/json/neo4jData.json", "w") as fp:
        json.dump(neo_graph, fp)
    return

def parse_chess():
    nodes = neo_graph["results"][0]["data"][0]["graph"]["nodes"]
    for k, data in chess["data"].items():
        # TODO(makdon): 还需要处理羁绊
        node = {
            "id": data["name"],
            "image": data["picture"],
            "labels": [],
            "properties": data
        }
        nodes.append(node)
    pass

def parse_job():
    nodes = neo_graph["results"][0]["data"][0]["graph"]["nodes"]
    for k, data in job["data"].items():
        node = {
            "id": data["name"],
            "image": data["picture"],
            "labels": [],
            "properties": data
        }
        nodes.append(node)

def parse_race():
    nodes = neo_graph["results"][0]["data"][0]["graph"]["nodes"]
    for k, data in race["data"].items():
        node = {
            "id": data["name"],
            "image": data["picture"],
            "labels": [],
            "properties": data
        }
        nodes.append(node)

def parse_trait():
    nodes = neo_graph["results"][0]["data"][0]["graph"]["nodes"]
    for k, data in trait["data"].items():
        node = {
            "id": data["name"],
            "image": data["picture"],
            "labels": [],
            "properties": data
        }
        nodes.append(node)


if __name__ == "__main__":
    convert_to_neo4j_data()
