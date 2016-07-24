import pandas as pd
import sys
import time_columns_adder
import matplotlib.pyplot as plt
import numpy as np

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../spotify/data/songs.csv", encoding="utf-8")
scrobbles = df.drop("Date", axis=1)
scrobbles = time_columns_adder.add_time_columns(df, scrobbles)
scrobbles = scrobbles.drop(["Artist mbid", "Album mbid", "Track mbid", "year", "month"], axis=1)

days = range(1, 32, 1)
unique_artists_by_day = scrobbles.groupby(["day"])["Artist"].nunique()
dict = {}
for day in days:
    if day in unique_artists_by_day:
        dict[day] = unique_artists_by_day[day]
    else:
        dict[day] = 0

unique_artists_by_day = pd.DataFrame.from_dict(dict, orient="index")
unique_artists_by_day.columns = ["Plays"]

unique_tracks_by_day = scrobbles.groupby(["day"])["Track"].nunique()
dict = {}
for day in days:
    if day in unique_tracks_by_day:
        dict[day] = unique_tracks_by_day[day]
    else:
        dict[day] = 0

unique_tracks_by_day = pd.DataFrame.from_dict(dict, orient="index")
unique_tracks_by_day.columns = ["Plays"]

day_index = np.array(unique_tracks_by_day.index)
unique_tracks_by_day = np.array(unique_tracks_by_day.values)
unique_artists_by_day = np.array(unique_artists_by_day.values)
day_values = np.array([unique_tracks_by_day, unique_artists_by_day])
labels = ["Unique Tracks", "Unique Artists"]

for y_arr, label in zip(day_values, labels):
    plt.plot(day_index, y_arr, label=label)

plt.legend()
plt.show()


# ax = plays_by_day.plot(kind="line", marker=".", figsize=[12, 8], linewidth=3, alpha=0.6, color="#6A2C70")
#
# ax.set_ylabel("Play Count")
# ax.set_xlabel("")
# ax.set_title("Plays per day")
#
# plt.show()
