import pandas as pd
import sys
import musicbrainzngs
import json
import os
import io
reload(sys)
sys.setdefaultencoding("utf8")

area_cache_path = "cache/area_cache.js"
artist_cache_path = "cache/artist_cache.js"
csv_path = "data/musicbrainz.csv"

cache_save_frequency = 10
area_requests_count = 0
artist_requests_count = 0

def load_file(path):
    if os.path.isfile(path):
        cache_file = json.load(open(path))
    else:
        cache_file = {}
    return cache_file

def save_cache_to_disk(cache, filepath):
    with io.open(filepath, "wb") as cache_file:
        cache_file.write(json.dumps(cache))

artist_cache = load_file(artist_cache_path)
area_cache = load_file(area_cache_path)

musicbrainzngs.set_useragent("MyMusicHistory", "1.0.0", "goktugercegurel@gmail.com")


def extract_artist_details(response):
    artist = response["artist"]

    artist_details = {"id": artist["id"],
                      "name": artist["name"],
                      "type": None,
                      "area_id": None,
                      "area_name": None,
                      "begin_area_id": None,
                      "begin_area_name": None,
                      "place_id": None,
                      "place": None}

    if "type" in artist:
        artist_details["type"] = artist["type"]

    if "area" in artist and artist["area"] is not None and "id" in artist["area"] and "name" in artist["area"]:
        artist_details["area_id"] = artist["area"]["id"]
        artist_details["area_name"] = artist["area"]["name"]

    if "begin-area" in artist and artist["begin-area"] is not None and "id" in artist["begin-area"] and "name" in \
            artist["begin-area"]:
        artist_details["begin_area_id"] = artist["begin-area"]["id"]
        artist_details["begin_area_name"] = artist["begin-area"]["name"]

    # if there is a begin area, then place is that. if there is not a begin are
    # but there is an area, then the area is that.
    if artist_details["begin_area_name"] is not None:
        artist_details["place"] = artist_details["begin_area_name"]
        artist_details["place_id"] = artist_details["begin_area_id"]
    elif artist_details["area_name"] is not None:
        artist_details["place"] = artist_details["area_name"]
        artist_details["place_id"] = artist_details["area_id"]

    return artist_details


def get_artist_by_id(artist_id):
    global artist_cache, artist_requests_count

    # check if I already saved the artist
    if artist_id in artist_cache:
        artist_details = artist_cache[artist_id]

    else:
        try:
            result = musicbrainzngs.get_artist_by_id(artist_id)
        except musicbrainzngs.WebServiceError as exc:
            print("Something went wrong with the request: %s" % exc)
            return
        else:
            artist_details = extract_artist_details(result)
            artist_cache[artist_id] = artist_details

            artist_requests_count += 1
            if artist_requests_count % cache_save_frequency == 0:
                save_cache_to_disk(artist_cache, artist_cache_path)

    return artist_details

iron_maiden_details = get_artist_by_id("ca891d65-d9b0-4258-89f7-e6ba29d83767")
print(json.dumps(iron_maiden_details, indent=2))


def create_artists_dataframe(artist_ids, csv_save_frequency=100):
    cols = ["id", "name", "type", "area_id", "area_name", "begin_area_id", "begin_area_name", "place_id", "place"]

    df = pd.DataFrame(columns=cols)

    n = 0
    for artist_id in artist_ids:
        try:
            artist = get_artist_by_id(artist_id)
            df.loc[n] = [artist[col] for col in cols]
            n += 1

            if n % (csv_save_frequency * 3) == 0:
                print("{}".format(n))
                df.to_csv(csv_path, index=False, encoding='utf-8')

        except Exception as e:
            pass

    df.to_csv(csv_path, index=False, encoding='utf-8')

    return df

scrobbles = pd.read_csv("data/all_scrobbles_last.csv", encoding="utf-8")
artist_ids = scrobbles["Artist mbid"].dropna().unique()

df = create_artists_dataframe(artist_ids)
df.to_csv(csv_path, index=False, encoding='utf-8')

print("artists data frame done")


def extract_area_details(response):
    area_details = {}
    area = response["area"]

    area_details["name"] = area["name"]
    if "area-relation-list" in area:
        for relation in area["area-relation-list"]:
            if "direction" in relation and relation["direction"] == "backward" and relation["type"] == "part of":
                area_details["parent_id"] = relation["area"]["id"]
                area_details["parent_name"] = relation["area"]["name"]
        return area_details

    return None


def get_area(area_id, full_area=""):
    global area_cache, area_requests_count

    if area_id in area_cache:
        area_details = area_cache[area_id]
    else:
        response = musicbrainzngs.get_area_by_id(area_id, includes=["area-rels"])
        area_details = extract_area_details(response)
        area_cache[area_id] = area_details

        area_requests_count += 1
        if area_requests_count % cache_save_frequency == 0:
            save_cache_to_disk(area_cache, area_cache_path)

    try:
        if full_area == "":
            full_area = area_details["name"]

        if "parent_name" in area_details and "parent_id" in area_details:
            full_area = "{}, {}".format(full_area, area_details["parent_name"])
            return area_details["parent_id"], full_area
        else:
            return None, full_area
    except Exception as e:
        return None, full_area

def get_place_full_name_by_area_id(area_id):
    area_name = ""
    while area_id is not None:
        area_id, area_name = get_area(area_id, area_name)
    return area_name


def get_full_place_names(unique_place_ids):
    place_ids_names = {}

    for place_id in unique_place_ids:
        try:
            place_name = get_place_full_name_by_area_id(place_id)
        except:
            place_name = None

        place_ids_names[place_id] = place_name

    return place_ids_names


def get_place_from_dict(place_id):
    try:
        return place_ids_names[place_id]
    except:
        return None

unique_place_ids = df["place_id"].dropna().unique()
place_ids_names = get_full_place_names(unique_place_ids)

df["place_full"] = df["place_id"].apply(get_place_from_dict)

df.to_csv(csv_path, index=False, encoding='utf-8')
save_cache_to_disk(area_cache, area_cache_path)
save_cache_to_disk(artist_cache, artist_cache_path)

import re
import time
import requests

pause_nominatim = 1.0
output_file = "data/coordinates.csv"

base_url = "https://nominatim.openstreetmap.org/search?format=json&q={}"

coordinate_cache_path = "cache/coordinate_cache.js"
coordinate_cache = load_file(coordinate_cache_path)
coordinate_requests_count = 0


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
    global coordinate_cache, coordinate_requests_count

    if place_name in coordinate_cache:
        return coordinate_cache[place_name]
    else:
        time.sleep(pause_nominatim)
        coordinate_requests_count += 1

        url = base_url.format(place_name)
        data = make_request(url)
        if len(data) > 0:
            coords = data[0]["lat"], data[0]["lon"]
        else:
            return

        coordinate_cache[place_name] = coords

        if coordinate_requests_count % cache_save_frequency == 0:
            save_cache_to_disk(coordinate_cache, coordinate_cache_path)

        return coords


regex = re.compile('\\(.*\\)|\\[.*\\]')


def clean_place_full(place_full):
    if isinstance(place_full, str):
        return regex.sub('', place_full).replace(' ,', ',').replace('  ', ' ')

df["place_full"] = df["place_full"].map(clean_place_full)

df.loc[df["place_full"]=="", "place_full"] = None
places = pd.Series(df["place_full"].dropna().sort_values().unique())

latlng_dict = {}
for place in places:
    latlng_dict[place] = find_coordinates(place)

def get_latlng_by_address(address):
    try:
        return latlng_dict[address]
    except:
        return None

df['place_latlng'] = df['place_full'].map(get_latlng_by_address)
df.to_csv(csv_path, index=False, encoding='utf-8')