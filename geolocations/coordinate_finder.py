# -*- coding: utf-8 -*-
import pandas as pd
import time
import requests
import json
import os.path
import datetime
import sys
from countryinfo import *
import request_utils

reload(sys)
sys.setdefaultencoding("utf8")

# sleep time between consecutive requests to api
pause_osm = 1.0

base_url = "https://nominatim.openstreetmap.org/search?format=json&q={}"

input_file = "data/info.csv"
output_file = "data/coordinates.csv"
cache_file = "data/coordinates_cache.js"
cache_save_frequency = 10
requests_count = 0

if os.path.isfile(cache_file):
    coordinates_cache = json.load(open(cache_file))
else:
    coordinates_cache = {}


def make_request(url):
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if request.status_code != 200:
        raise requests.ConnectionError("Expected status code 200, but got {}".format(request.status_code))

    response = request.json()
    return response


def find_coordinates(place_name):
    global coordinates_cache, requests_count

    if place_name in coordinates_cache:
        return coordinates_cache[place_name]
    else:
        time.sleep(pause_osm)
        requests_count += 1

        url = base_url.format(place_name)
        data = make_request(url)
        if len(data) > 0:
            coords = data[0]["lat"], data[0]["lon"]
        else:
            return

        coordinates_cache[place_name] = coords

        if requests_count % cache_save_frequency == 0:
            request_utils.save_cache_to_disk(coordinates_cache, cache_file)

        return coords


def get_coordinates():
    df = pd.read_csv("data/info.csv", encoding="utf-8")
    places = pd.Series(df["place"].dropna().sort_values().unique())

    coords_dict = {}
    for place in places:
        if check_if_country(place):
            continue
        coords = find_coordinates(place)
        if coords is not None:
            coords_dict[place] = coords
            print(coords)

    df = pd.Series(coords_dict, name="Coordinates")
    df.index.name = "Place"
    df = df.reset_index()
    print(df.head())
    df.to_csv("data/coordinates.csv", index=None, encoding="utf-8")


df = pd.read_csv("data/coordinates.csv", encoding="utf-8")
split_df = df["Coordinates"].apply(lambda x: pd.Series(x.split(",")))
split_df.columns=["Latitude", "Longitude"]
split_df.to_csv("data/coordinates_split.csv", index=None, encoding="utf-8")
