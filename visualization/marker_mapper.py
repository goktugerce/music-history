import pandas as pd
import sys
from html_template import *
from ast import literal_eval

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../data/musicbrainz.csv", encoding="utf-8")
df = df[["name", "place", "place_full", "place_latlng"]]
df.dropna(axis=0, how="any", inplace=True)

scrobbles = pd.read_csv("../data/lastfm_all_scrobbles.csv", encoding="utf-8")
top_tracks = scrobbles["Artist"].value_counts()
top_tracks = pd.DataFrame(top_tracks)
top_tracks = top_tracks.reset_index()
top_tracks.columns = ["Artist", "Play Count"]
df["play_count"] = 0

for index, row in df.iterrows():
    values = top_tracks[top_tracks["Artist"] == row["name"]]["Play Count"].values
    if (len(values) > 0):
        df.loc[index, "play_count"] = top_tracks[top_tracks["Artist"] == row["name"]]["Play Count"].values[0]

df = df.sort_values(["play_count"], ascending="False")

def to_html(row):
    latlng = literal_eval(row["place_latlng"])
    name = row["name"]
    place = row["place"]
    count = row["play_count"]

    string = "data.addRows([["
    string += str(latlng[0]) + ","
    string += str(latlng[1]) + ","
    string += "'" + name.replace("\'", "\\'") + "', "
    string += str(count) + ","
    string += "'" + place.replace("\'", "\\'") + "']]);"

    return string

df["html"] = df.apply(to_html, axis = 1)
uk = df[df["place_full"].str.contains("United Kingdom")]
us = df[df["place_full"].str.contains("United States")]

html_data = ""

for index, row in df["html"].iteritems():
    html_data += row + "\n"

html_data = html_data[:-2]

html = html_map_marker.format(html_data, "world");

f = open("world_map.html", "w")
f.write(html)
f.close()


html_uk_data = ""
for index, row in uk["html"].iteritems():
    html_uk_data += row + "\n"

html_uk_data = html_uk_data[:-2]

html = html_map_marker.format(html_uk_data, "GB");

f = open("uk_map.html", "w")
f.write(html)
f.close()

html_us_data = ""
for index, row in us["html"].iteritems():
    html_us_data += row + "\n"

html_us_data = html_us_data[:-2]

html = html_map_marker.format(html_us_data, "US");

f = open("us_map.html", "w")
f.write(html)
f.close()