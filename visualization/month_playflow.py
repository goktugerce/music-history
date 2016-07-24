import pandas as pd
import sys
import time_columns_adder
import matplotlib.pyplot as plt
import numpy as np
import datetime
from html_template import *

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../spotify/data/songs.csv", encoding="utf-8")
scrobbles = df.drop("Date", axis=1)
scrobbles = time_columns_adder.add_time_columns(df, scrobbles)
scrobbles = scrobbles.drop(["Artist mbid", "Album mbid", "Track mbid", "year", "month"], axis=1)
scrobbles["duration_min"] = ((scrobbles["Duration"] / 1000) / 60).astype(int)
scrobbles["duration_sec"] = ((scrobbles["Duration"] / 1000) % 60).astype(int)


def add_song_duration(row):
    start_date = row["timestamp"].to_datetime()
    min = row["duration_min"]
    sec = row["duration_sec"]
    end_date = start_date + datetime.timedelta(minutes=min, seconds=sec)
    return end_date


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def add_html_tag(row):
    start = row["timestamp"].to_datetime()
    end = row["endtime"].to_datetime()
    if start.day == end.day:
        string = "['"
        string += "May " + str(start.day)
        string += "', '" + row["Artist"].replace("'", "\\\'") + " - " + row["Track"].replace("'", "\\\'")
        string += "', new Date(2016,01,01, " + str(start.hour) + "," + str(start.minute) + ',' + str(
            start.second) + '),'
        string += " new Date(2016,01,01, " + str(end.hour) + "," + str(end.minute) + ',' + str(end.second) + ')'
        string += "]"
    else:
        string = "['"
        string += "May " + str(start.day)
        string += "', '" + row["Artist"].replace("'", "\\\'") + " - " + row["Track"].replace("'", "\\\'")
        string += "', new Date(2016,01,01, " + str(start.hour) + "," + str(start.minute) + ',' + str(
            start.second) + '),'
        string += " new Date(2016,01,01, " + "23" + "," + "59" + ',' + "59" + ')'
        string += "],"
        string += "['"
        string += "May " + str(end.day)
        string += "', '" + row["Artist"].replace("'", "\\\'") + " - " + row["Track"].replace("'", "\\\'")
        string += "', new Date(2016,01,01, " + "0" + "," + "0" + ',' + "0" + '),'
        string += " new Date(2016,01,01, " + str(end.hour) + "," + str(end.minute) + ',' + str(end.second) + ')'
        string += "]"
    return string


count = 0


def shift_time(row):
    global count
    if row["endtime"] > row["next_start"]:
        return row["next_start"]
    else:
        return row["endtime"]


scrobbles["endtime"] = scrobbles.apply(add_song_duration, axis=1)
scrobbles["next_start"] = scrobbles["timestamp"].shift(1)
scrobbles["endtime"] = scrobbles.apply(shift_time, axis=1)

scrobbles["html"] = scrobbles.apply(add_html_tag, axis=1)
html_data = ""
for index, row in scrobbles["html"].iteritems():
    html_data += row + ",\n"

html_data = html_data[:-2]
html = month_html.format(html_data)

f = open("month_playflow.html", "w")
f.write(html)
f.close()
