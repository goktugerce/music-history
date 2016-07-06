import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../data/top_tracks.csv", encoding="utf-8")
index = df.apply(lambda x: "{}\n{}".format(x["Artist"], x["Track"]), axis=1)
df = df.set_index(index).drop(labels=["Artist", "Track"], axis=1)
top_tracks = df["Play Count"].head(20).sort_values()
top_track_genres = df.drop("Play Count", axis=1).stack().head(20).value_counts().head(10)

sns.set_context("notebook", font_scale=1.3, rc={"lines.linewidth": 2.5})

def plot_tracks():
    ax = top_tracks.plot(kind="barh", figsize=[8, 12], alpha=0.8, width=0.85, color="#6A2C70", edgecolor="w")

    ax.set_title("Top Tracks")
    ax.set_xlabel("Play Count")

    plt.savefig("../images/top_tracks.png", dpi=96, bbox_inches="tight")
    plt.show()


def plot_genres():
    flatui = ["#85144B", "#0074D9", "#7FDBFF", "#39CCCC", "#3D9970", "#2ECC40", "#01FF70", "#FFDC00", "#FF851B",
              "#FF4136"]
    explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    sns.set_palette(flatui)

    ax = top_track_genres.plot(kind="pie", figsize=[8, 8], shadow=True, startangle=250, explode=explode[:len(top_track_genres.index)])

    ax.set_title("Top Genres", y=1.03)
    ax.set_xlabel("")
    ax.set_ylabel("")

    plt.savefig("../images/top_track_genres.png", dpi=96, bbox_inches="tight")
    plt.axis("equal")
    plt.show()


plot_genres()
