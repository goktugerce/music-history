import spotipy
import spotipy.util as util
import os
import json
import pandas as pd
import sys
import spotify_utils
import time
import youtube_search

reload(sys)
sys.setdefaultencoding("utf8")

# define constants
spotify = spotipy.Spotify()
pause_duration = 0.25
base_q = "track:\"{}\" artist:\"{}\" album:\"{}\""

# variables to store cache every x times
requests_count = 0
cache_save_frequency = 10


def get_duration(track, artist, album, is_clean):
    global requests_count
    requests_count += 1

    if is_clean:
        q = base_q.format(track, artist, album)
    else:
        q = get_cleaned_q(track, artist, album)

    if q in song_cache:
        print("{} out of {} - {}: {} milliseconds".format(requests_count + 1, df.shape[0], track, song_cache[q]))
        return song_cache[q]

    # time.sleep(pause_duration)

    results = spotify.search(q=q, type="track")

    if len(results["tracks"]["items"]) == 0:
        return

    duration = results["tracks"]["items"][0]["duration_ms"]
    song_cache[q] = duration
    print("{} out of {} - {}: {} milliseconds".format(requests_count + 1, df.shape[0], track, song_cache[q]))

    if requests_count % cache_save_frequency == 0:
        spotify_utils.save_cache_to_disk(song_cache)
    return duration


def get_duration_from_lastfm(mbid):
    global requests_count
    requests_count += 1
    if mbid in song_cache:
        print("{} out of {} - {} milliseconds".format(requests_count + 1, df.shape[0], song_cache[mbid]))
        return song_cache[mbid]

    time.sleep(pause_duration)

    response = spotify_utils.get_response(mbid)
    duration = response["track"]["duration"]

    song_cache[mbid] = duration
    print("{} out of {} - {} milliseconds".format(requests_count + 1, df.shape[0], song_cache[mbid]))
    if requests_count % cache_save_frequency == 0:
        spotify_utils.save_cache_to_disk(song_cache)
    return duration


def get_duration_from_youtube(q):
    global requests_count
    requests_count += 1

    if q in song_cache:
        print("{} out of {} - {} milliseconds".format(requests_count + 1, df.shape[0], song_cache[q]))
        return song_cache[q]

    duration = youtube_search.youtube_search(q)
    song_cache[q] = duration
    print("{} out of {} - {} milliseconds".format(requests_count + 1, df.shape[0], song_cache[q]))
    if requests_count % cache_save_frequency == 0:
        spotify_utils.save_cache_to_disk(song_cache)
    return duration


def title_cleaner(string):
    first_dash = string.find("[")
    first_parenthesis = string.find("(")
    if first_dash != -1 and first_parenthesis != -1:
        min_index = min(first_dash, first_parenthesis)
        return string[:min_index]
    if first_dash == -1 and first_parenthesis == -1:
        return string
    if first_dash != -1:
        return string[:first_dash]
    return string[:first_parenthesis]


def get_cleaned_q(track, artist, album):
    track = title_cleaner(track)
    artist = title_cleaner(artist)
    album = title_cleaner(album)
    q = base_q.format(track, artist, album)
    return q


foo = lambda x: get_duration(x["Track"], x["Artist"], x["Album"], x["Duration"] > 0)

song_cache = spotify_utils.get_cache()
# df = pd.read_csv("../data/2016-05.csv", encoding="utf-8")
# df["Duration"] = df.apply(lambda x: get_duration(x["Track"], x["Artist"], x["Album"], True), axis=1)
# spotify_utils.save_cache_to_disk(song_cache)
# df.to_csv("data/songs.csv", index=None, encoding="utf-8")


df = pd.read_csv("data/songs.csv", encoding="utf-8")

# df["Duration"] = df.apply(foo, axis=1)
# spotify_utils.save_cache_to_disk(song_cache)
# df.to_csv("data/songs.csv", encoding="utf-8", index=None)
#
# df[df["Duration"].isnull() & df["Track mbid"].notnull()] = df[
#     df["Duration"].isnull() & df["Track mbid"].notnull()].apply(
#     lambda x: get_duration_from_lastfm(x["Track mbid"]), axis=1)

# for index, row in df[df["Duration"].isnull() & df["Track mbid"].notnull()].iterrows():
#     duration = get_duration_from_lastfm(row["Track mbid"])
#     df.loc[index, "Duration"] = duration

# for index, row in df[df["Duration"].isnull()].iterrows():
#     q = "{} {}".format(row["Artist"], row["Track"])
#     if row["Track"] == "Music":
#         q = "{} {} {}".format(row["Artist"], row["Track"], row["Album"])
#
#     print(q)
#     duration = get_duration_from_youtube(q)
#     df.loc[index, "Duration"] = duration
#
# spotify_utils.save_cache_to_disk(song_cache)
# df.to_csv("data/songs.csv", index=None, encoding="utf-8")
