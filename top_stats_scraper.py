import os
import time
import sys

import requests
import pandas as pd

import tag_scraper

base_url = "http://ws.audioscrobbler.com/2.0/?method=user.get{}&user={}&api_key={}&limit={}&format=json"
api_key = os.environ["LASTFM_API_KEY"]
user = "goktugerce"
limit = "100"
pause_duration = 0.1

reload(sys)
sys.setdefaultencoding("utf8")


def get_response(method):
    """
    Formats the string, makes the GET request and returns the response
    :param method: API method for the URL
    :return: response
    """
    url = base_url.format(method, user, api_key, limit)
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if request.status_code != 200:
        raise requests.ConnectionError("Expected status code 200, but got {}".format(request.status_code))

    response = request.json()

    return response


def get_top_artists():
    """
    Get top artists and save names, play counts and genres.
    :return:
    """
    method = "topartists"
    response = get_response(method)

    artists = []
    play_counts = []
    tag1 = []
    tag2 = []
    tag3 = []

    for artist in response[method]["artist"]:
        artists.append(artist["name"])
        play_counts.append(artist["playcount"])
        tags = tag_scraper.get_artist_tags(artist["mbid"])
        if len(tags) == 0:
            continue
        tag1.append(tags[0])
        tag2.append(tags[1])
        tag3.append(tags[2])
        time.sleep(pause_duration)

    data_set = list(zip(artists, play_counts, tag1, tag2, tag3))
    df = pd.DataFrame(data=data_set, columns=["Artist", "Play Count", "Tag1", "Tag2", "Tag3"])
    df.to_csv("data/top_artists.csv", index=None, encoding="utf-8")


def get_top_albums():
    """
    Get top albums and save names, play counts, artists and genres.
    :return:
    """
    method = "topalbums"
    response = get_response(method)

    albums = []
    play_counts = []
    artists = []
    tag = []

    for album in response[method]["album"]:
        albums.append(album["name"])
        play_counts.append(album["playcount"])
        artists.append(album["artist"]["name"])
        tag.append(tag_scraper.get_album_tag(album["mbid"]))
        time.sleep(pause_duration)

    data_set = list(zip(albums, artists, play_counts, tag))
    df = pd.DataFrame(data=data_set, columns=["Album", "Artist", "Play Count", "Tag"])
    df.to_csv("data/top_albums.csv", index=None, encoding="utf-8")


def get_top_tracks():
    """
    Get top tracks and save names, artists, play counts and genres.
    :return:
    """
    method = "toptracks"
    response = get_response(method)

    tracks = []
    artists = []
    play_counts = []
    tag1 = []
    tag2 = []
    tag3 = []

    for track in response[method]["track"]:
        track_name = track["name"]
        artist = track["artist"]["name"]

        tracks.append(track_name)
        artists.append(artist)
        play_counts.append(track["playcount"])
        tags = tag_scraper.get_track_tags(artist, track_name)

        if tags is None:
            continue
        elif len(tags) == 1:
            tag1.append(tags[0])
        elif len(tags) == 2:
            tag1.append(tags[0])
            tag2.append(tags[1])
        elif len(tags) == 3:
            tag1.append(tags[0])
            tag2.append(tags[1])
            tag3.append(tags[2])

        time.sleep(pause_duration)

    data_set = list(zip(tracks, artists, play_counts, tag1, tag2, tag3))
    df = pd.DataFrame(data=data_set, columns=["Track", "Artist", "Play Count", "Tag1", "Tag2", "Tag3"])
    df.to_csv("data/top_tracks.csv", index=None, encoding="utf-8")


get_top_albums()
get_top_tracks()