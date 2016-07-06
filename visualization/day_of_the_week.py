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

day_counts = scrobbles["weekday"].value_counts().sort_index()
day_counts.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

ax = day_counts.plot(kind="bar", figsize=[6, 4], width=0.85, alpha=0.6, color="#FF165D")
ax.set_xticklabels(day_counts.index, rotation=45, rotation_mode="anchor", ha="right")

ax.set_title("Plays per day of the week")
ax.set_xlabel("")
ax.set_ylabel("Play Count")

plt.savefig("../images/day_of_the_week.png", dpi=96, bbox_inches="tight")
plt.show()
