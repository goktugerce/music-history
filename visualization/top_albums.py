import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from html_template import *

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../data/top_albums.csv", encoding="utf-8")
index = df.apply(lambda x: "{}\n{}".format(x["Artist"], x["Album"]), axis=1)
df = df.set_index(index).drop(labels=["Artist", "Album"], axis=1)
top_albums = df["Play Count"].head(20).sort_values()
top_album_genres = df.drop("Play Count", axis=1).stack().head(20).value_counts().head(10)

sns.set_context("notebook", font_scale=1.3, rc={"lines.linewidth": 2.5})


def plot_albums():
    ax = top_albums.plot(kind="barh", figsize=[8, 12], alpha=0.8, width=0.85, color="#3490DE", edgecolor="w")

    ax.set_title("Top Albums")
    ax.set_xlabel("Play Count")

    plt.savefig("../images/top_albums.png", dpi=96, bbox_inches="tight")
    plt.show()


def plot_genres():
    flatui = ["#85144B", "#0074D9", "#7FDBFF", "#39CCCC", "#3D9970", "#2ECC40", "#01FF70", "#FFDC00", "#FF851B",
              "#FF4136"]
    explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    sns.set_palette(flatui)

    ax = top_album_genres.plot(kind="pie", figsize=[8, 8], shadow=True, startangle=250, explode=explode)

    ax.set_title("Top Genres", y=1.03)
    ax.set_xlabel("")
    ax.set_ylabel("")

    plt.savefig("../images/top_album_genres.png", dpi=96, bbox_inches="tight")
    plt.axis("equal")
    plt.show()


def make_html(row):
    string = "['"
    string += row["Album"].replace("\'", "\\'")
    string += "',"
    string += str(row["Play Count"])
    string += "]"
    return string


top_albums = top_albums.reset_index()
top_albums.columns = ["Album", "Play Count"]

top_albums["html"] = top_albums.apply(make_html, axis=1)

html_album_data = ""
for index, row in top_albums["html"].sort_index(ascending=False).iteritems():
    html_album_data += row.replace("\n", " - ") + ",\n"

html_album_data = html_album_data[:-2]

html_genre_data = ""
for index, row in top_album_genres.iteritems():
    string = "['"
    string += index
    string += "',"
    string += str(row)
    string += "]"
    html_genre_data += string + ",\n"

html_genre_data = html_genre_data[:-2]

html = html_top_albums_and_tracks.format("Albums", "'Album'", html_album_data, "#3490DE", "Albums",
                                         html_genre_data, "Albums")

f = open("top_albums.html", "w")
f.write(html)
f.close()
