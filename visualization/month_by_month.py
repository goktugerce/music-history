import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np
import random

import time_columns_adder

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../data/all_scrobbles.csv", encoding="utf-8")
scrobbles = df.drop("Date", axis=1)
scrobbles = time_columns_adder.add_time_columns(df, scrobbles)

month_counts = scrobbles["month"].value_counts().sort_index()

ax = month_counts.plot(kind="line", marker=".", figsize=[12, 8], linewidth=3, alpha=0.6, color="#6A2C70")

xlabels = month_counts.iloc[range(0, len(month_counts), 3)].index
xlabels = [x if x in xlabels else "" for x in month_counts.index]
ax.set_xticks(range(len(xlabels)))
ax.set_xticklabels(xlabels, rotation=45, rotation_mode='anchor', ha='right')

ax.set_ylabel("Play Count")
ax.set_xlabel("")
ax.set_title("Plays per month, {}-{}".format(min(scrobbles["year"]), max(scrobbles["year"])))

play_counts = np.array(month_counts.values)
top_indices = play_counts.argsort()[-3:][::-1]
top_values = [play_counts[x] for x in top_indices]

"""
Add annotations to three months with most songs played
"""
for i in range(3):
    if i == 1:
        coeff = 1.1
    else:
        coeff = 0.9
    ax.annotate(top_values[i], xy=(top_indices[i], top_values[i]), xytext=(top_indices[i] - 2, top_values[i] * coeff),
                arrowprops=dict(facecolor="#B83B5E", shrink=0.1, width=2, headlength=10), color="#B83B5E"
                )

plt.savefig("../images/month_by_month.png", dpi=96, bbox_inches="tight")
plt.show()
