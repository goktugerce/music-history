import os
import requests
import re
import sys

reload(sys)
sys.setdefaultencoding("utf8")

artist_tag_base_url = "http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&mbid={}&api_key={}&format=json"
album_tag_base_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&mbid={}&api_key={}&format=json"
track_tag_base_url = "http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={}&track={}&autocorrect=1&api_key={}&format=json"

api_key = os.environ["LASTFM_API_KEY"]
user = "goktugerce"
limit = "100"
pause_duration = 0.2

disabled_tags = ["albums i own", "favourite albums", "favorite albums", "singer-songwriter", "favourites", "favorites",
                 "favorite songs", "seen live"]
year_regex = re.compile("^\d{4}$")


def get_response(url):
    """
    Formats the string, makes the GET request and returns the response
    :param method: API method for the URL
    :return: response
    """
    try:
        request = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    if request.status_code != 200:
        raise requests.ConnectionError("Expected status code 200, but got {}".format(request.status_code))

    response = request.json()

    return response


def get_artist_tags(mbid):
    """
    Finds top three tags of the artist
    :param mbid: unique id of the artist
    :return: top three tags of the artist
    """
    artist_tag_url = artist_tag_base_url.format(mbid, api_key)
    response = get_response(artist_tag_url)

    if "error" in response:
        return

    tags = []
    for tag in response["toptags"]["tag"]:
        tags.append(tag["name"])
    tags = tags[:3]
    return tags


def get_album_tag(mbid):
    """
    Find the album's genre. Returned tag should not be one of the following:
    albums I own, favourite albums, favorite albums, singer-songwriter, a year, artist's name, best of x
    :param mbid: unique id of the album
    :return: the top tag of the album
    """
    album_tag_url = album_tag_base_url.format(mbid, api_key)
    response = get_response(album_tag_url)

    if "error" in response:
        return

    for tag in response["album"]["tags"]["tag"]:
        if tag["name"].lower() not in disabled_tags and not year_regex.match(tag["name"]) and tag["name"] != \
                response["album"][
                    "artist"] and "best of" not in tag["name"].lower():
            return tag["name"]

    return


def get_track_tags(artist, track):
    """
    Find the track's top tags.
    Exclude tags with same name as artist and keywords such as "best of", "favourite, "favorite"
    :param artist: name of the artist or the band
    :param track: name of the track
    :return: top three tags
    """
    track_tag_url = track_tag_base_url.format(artist, track, api_key)
    response = get_response(track_tag_url)

    if "error" in response:
        return

    tags = []
    for tag in response["toptags"]["tag"]:
        if tag["name"] not in disabled_tags and tag["name"].lower() != artist.lower():
            tags.append(tag["name"])

    tags = tags[:3]
    return tags
