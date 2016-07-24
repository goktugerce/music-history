import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

import time_columns_adder
from html_template import *

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../data/all_scrobbles_last.csv", encoding="utf-8")
scrobbles = df.drop("Date", axis=1)
scrobbles = time_columns_adder.add_time_columns(df, scrobbles)

hour_counts = scrobbles["hour"].value_counts().sort_index()
ax = hour_counts.plot(kind="line", figsize=[12, 8], linewidth="3", alpha=0.8, marker="o", color="#00B8A9")

xlabels = hour_counts.index.map(lambda x: "{:02}:00".format(x))
ax.set_xticks(range(len(xlabels)))
ax.set_xticklabels(xlabels, rotation=45, rotation_mode="anchor", ha="right")

ax.set_xlabel("Hour", labelpad=20)
ax.set_ylabel("Plays", labelpad=20)
ax.set_title("Number of Plays by Hour")

# plt.savefig("../images/hour.png", dpi=96, bbox_inches="tight")
# plt.show()

html_data = ""
for index, row in hour_counts.iteritems():
    string = "['"
    hour = "{:02}:00".format(index)
    string += hour
    string += "',"
    string += str(row)
    string += "]"
    html_data += string + ",\n"

html_data = html_data[:-2]

html = html_line_chart.format("Hour of the day", "Hour", html_data, "#00B8A9", "Hours", "Music listening data by hour of the day")

f = open("hour_chart.html", "w")
f.write(html)
f.close()