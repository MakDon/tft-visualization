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
idToNameMap = {}

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
    parse_job()
    parse_race()
    parse_trait()
    parse_chess()
    # neo_graph["results"][0]["data"][0]["graph"]["relationships"] = []
    with open("./json/neo4jData.json", "w") as fp:
        json.dump(neo_graph, fp)
    with open("./neo4jd3/docs/json/neo4jData.json", "w") as fp:
        json.dump(neo_graph, fp)
    return

def parse_chess():
    nodes =         neo_graph["results"][0]["data"][0]["graph"]["nodes"]
    relationships = neo_graph["results"][0]["data"][0]["graph"]["relationships"]
    for k, data in chess["data"].items():
        # TODO(makdon): 还需要处理羁绊
        node = {
            "id": data["name"],
            "image": data["picture"],
            "labels": [data["name"]],
            "properties": data
        }
        nodes.append(node)
        classes = data["class"].split()
        for class_ in classes:
            class_ = idToNameMap.get(class_)
            if class_ is not None:
                rls = {
                    "id": data["name"] + "-" + class_,
                    "startNode": data["name"],
                    "endNode": class_,
                    "type": "has_class",
                    "properties": {
                        "id": data["name"] + "-" + class_,
                    }
                }
                relationships.append(rls)
        species = data["species"]
        species = idToNameMap.get(species)
        if species is not None:
            rls = {
                "id": data["name"] + "-" + species,
                "startNode": data["name"],
                "endNode": species,
                "type": "has_species",
                "properties": {
                    "id": data["name"] + "-" + species,
                }
            }
            relationships.append(rls)

        

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
        idToNameMap[data["id"]] = data["name"]

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
        idToNameMap[data["id"]] = data["name"]

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
        idToNameMap[data["id"]] = data["name"]


if __name__ == "__main__":
    convert_to_neo4j_data()
