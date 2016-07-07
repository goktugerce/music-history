import musicbrainzngs
import pandas as pd
import os
import json
import request_utils

area_cache_path = "data/area_cache.js"
artist_cache_path = "data/artist_cache.js"
csv_filename = "data/info.csv"

if os.path.isfile(artist_cache_path):
    artist_cache = json.load(open(artist_cache_path))
else:
    artist_cache = {}

musicbrainzngs.set_useragent("MyMusicHistory", "1.0.0", "goktugercegurel@gmail.com")
scrobbles = pd.read_csv("../data/all_scrobbles.csv", encoding="utf-8")
artist_ids = scrobbles["Artist mbid"].dropna().unique()

artist_requests_count = 0
area_requests_count = 0
cache_save_frequency = 10


def get_artist_details(artist_id):
    """
    Send request to musicbrainz api using musicbrainzngs module and save artist details
    :param artist_id: unique mbid of the artist
    :return: id, name, type and place details of the artist
    """
    global artist_requests_count

    if artist_id in artist_cache:
        artist_details = artist_cache[artist_id]
    else:
        try:
            result = musicbrainzngs.get_artist_by_id(artist_id)
        except musicbrainzngs.WebServiceError as exc:
            print("Something went wrong with the request: %s" % exc)
            return
        else:
            artist = result["artist"]

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
            if "begin-area" in artist and artist["begin-area"] is not None and "id" in artist[
                "begin-area"] and "name" in artist["begin-area"]:
                artist_details["begin_area_id"] = artist["begin-area"]["id"]
                artist_details["begin_area_name"] = artist["begin-area"]["name"]

            # populate place with begin-area_name if it"s not null, else area_name if it"s not null, else None
            if artist_details["begin_area_name"] is not None:
                artist_details["place"] = artist_details["begin_area_name"]
                artist_details["place_id"] = artist_details["begin_area_id"]
            elif artist_details["area_name"] is not None:
                artist_details["place"] = artist_details["area_name"]
                artist_details["place_id"] = artist_details["area_id"]

            artist_cache[artist_id] = artist_details

    artist_requests_count += 1
    if artist_requests_count % cache_save_frequency == 0:
        request_utils.save_cache_to_disk(artist_cache, artist_cache_path)
        print("saved cache")
    return artist_details


def create_data_frame(row_labels=None, df=None, csv_save_frequency=100):
    """
    Create data frame to store place ids
    :param row_labels: number of indices
    :param df: data frame
    :param csv_save_frequency: save it every n times
    :return: created data frame
    """
    if row_labels is None:
        row_labels = range(len(artist_ids))

    cols = ["id", "name", "type", "begin_area_id", "begin_area_name", "area_id", "area_name", "place_id", "place"]

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(columns=cols)

    for artist_id, n in zip(artist_ids, row_labels):
        artist = get_artist_details(artist_id)
        if artist is not None:
            df.loc[n] = [artist[col] for col in cols]
            if n % csv_save_frequency == 0: df.to_csv(csv_filename, index=False, encoding="utf-8")
            print("{} is done".format(n))

    return df


df = pd.read_csv("data/info.csv", encoding="utf-8")
print(df.head())
