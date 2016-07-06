import os
import requests
import time
import sys

import pandas as pd

reload(sys)
sys.setdefaultencoding("utf8")

api_key = os.environ["LASTFM_API_KEY"]
user = "goktugerce"
limit = "500"
pause_duration = 0.2
extended = 0

url = "https://ws.audioscrobbler.com/2.0/?method=user.get{}&user={}&api_key={}&limit={}&extended={}&page={}&format=json"


def find_total_pages(url):
    """
    Find total number of pages to traverse
    :param url: request url
    :return: total number of pages
    """
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if request.status_code != 200:
        raise requests.ConnectionError("Expected status code 200, but got {}".format(request.status_code))

    response = request.json()
    total_pages = int(response["recenttracks"]["@attr"]["totalPages"])
    return total_pages


def get_all_scrobbles(method="recenttracks", username=user, key=api_key, limit=limit, page=1,
                      extended=extended):
    """
    Traverse through all pages of user scrobbles and save artist,album and track names and mbids, and also a timestamp.
    :param method: recenttracks
    :param username: user to be explored
    :param key: api key to use
    :param limit: how many tracks in a page
    :param page: number of the page
    :param extended: include extended data for artist and albums or not
    :return:
    """
    responses = []
    artist_names = []
    artist_mbids = []
    album_names = []
    album_mbids = []
    track_names = []
    track_mbids = []
    timestamps = []

    request_url = url.format(method, username, key, limit, extended, page)
    total_pages = find_total_pages(request_url)

    for page in range(1, total_pages + 1):
        if page % 5 == 0:
            print("Page {} is done".format(page))
        time.sleep(pause_duration)
        request_url = url.format(method, username, key, limit, extended, page)
        responses.append(requests.get(request_url))

    for response in responses:
        scrobbles = response.json()

        for scrobble in scrobbles[method]["track"]:
            if "date" in scrobble:
                artist_names.append(scrobble["artist"]["#text"])
                artist_mbids.append(scrobble["artist"]["mbid"])
                album_names.append(scrobble["album"]["#text"])
                album_mbids.append(scrobble["album"]["mbid"])
                track_names.append(scrobble["name"])
                track_mbids.append(scrobble["mbid"])
                timestamps.append(scrobble["date"]["uts"])

    data_set = list(zip(artist_names, artist_mbids, album_names, album_mbids, track_names, track_mbids))
    df = pd.DataFrame(data=data_set, columns=["Artist", "Artist mbid", "Album", "Album mbid", "Track", "Track mbid"])
    df["Date"] = timestamps
    df["Date"] = pd.to_datetime(df["Date"].astype(int), unit="s")
    df.to_csv("data/all_scrobbles.csv", index=None, encoding="utf-8")


get_all_scrobbles()
