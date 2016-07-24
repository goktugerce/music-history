import os
import json
import requests
import sys

cache_path = "song_cache.js"
base_url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&mbid={}&api_key={}&format=json"
api_key = os.environ["LASTFM_API_KEY"]
pause_duration = 0.1


# define cache and load it
def get_cache():
    if os.path.isfile(cache_path):
        song_cache = json.load(open(cache_path))
    else:
        song_cache = {}
    return song_cache


def save_cache_to_disk(cache):
    with open(cache_path, "wb") as cache_file:
        cache_file.write(json.dumps(cache))
    print("saved {:,} cached items to {}".format(len(cache.keys()), cache_path))


def get_response(mbid):
    """
    Formats the string, makes the GET request and returns the response
    :param method: API method for the URL
    :return: response
    """
    url = base_url.format(mbid, api_key)
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if request.status_code != 200:
        raise requests.ConnectionError("Expected status code 200, but got {}".format(request.status_code))

    response = request.json()

    return response
