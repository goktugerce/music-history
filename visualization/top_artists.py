import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from html_template import *

reload(sys)
sys.setdefaultencoding("utf8")

top_artists = pd.read_csv("../data/top_artists.csv", encoding="utf-8")
top_artists = top_artists.set_index("Artist").head(25)
genres = top_artists.drop("Play Count", axis=1).stack().value_counts().head(10)

sns.set_context("notebook", font_scale=1.3, rc={"lines.linewidth": 2.5})


def plot_artists():
    ax = top_artists.plot(kind="bar", figsize=[12, 8], alpha=0.8, width=0.85, color="#EA5455", edgecolor="w")
    ax.set_xticklabels(top_artists.index, rotation=45, rotation_mode="anchor", ha="right")

    ax.set_title("Top Artists")
    plt.savefig("../images/top_artists.png", dpi=96, bbox_inches="tight")
    plt.show()


def plot_genres():
    flatui = ["#85144B", "#0074D9", "#7FDBFF", "#39CCCC", "#3D9970", "#2ECC40", "#01FF70", "#FFDC00", "#FF851B",
              "#FF4136"]

    explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    sns.set_palette(flatui)

    ax = genres.plot(kind="pie", figsize=[8, 8], shadow=True, startangle=250, explode=explode[:len(genres.index)])
    ax.set_title("Top Genres", y=1.03)
    ax.set_xlabel("")
    ax.set_ylabel("")

    plt.savefig("../images/top_artist_genres.png", dpi=96, bbox_inches="tight")
    plt.axis("equal")
    plt.show()


def make_html(row):
    string = "['"
    string += row["Artist"]
    string += "',"
    string += str(row["Play Count"])
    string += "]"
    return string


top_artists = top_artists.reset_index()
top_artists["html"] = top_artists.apply(make_html, axis=1)

html_artist_data = ""
for index, row in top_artists["html"].iteritems():
    html_artist_data += row + ",\n"

html_artist_data = html_artist_data[:-2]

html_genre_data = ""
for index, row in genres.iteritems():
    string = "['"
    string += index
    string += "',"
    string += str(row)
    string += "]"
    html_genre_data += string + ",\n"

html_genre_data = html_genre_data[:-2]

html = html_top_artists.format(html_artist_data, html_genre_data)

f = open("top_artists.html", "w")
f.write(html)
f.close()
