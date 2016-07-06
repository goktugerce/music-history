import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

import time_columns_adder

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../data/all_scrobbles.csv", encoding="utf-8")
scrobbles = df.drop("Date", axis=1)
scrobbles = time_columns_adder.add_time_columns(df, scrobbles)

scrobbles["exact_hour"] = scrobbles["hour"].astype(int) + scrobbles["minute"].astype(int) / 60

df = pd.DataFrame(columns=["Hour", "Weekday"])
df["Hour"] = scrobbles["exact_hour"]
df["Weekday"] = scrobbles["weekday"]

ax = sns.violinplot(x="Weekday", y="Hour", data=df, inner="quartiles", cut=0)
ax.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rotation=45,
                   rotation_mode="anchor", ha="right")
ax.set_xlabel("Days", labelpad=20)
ax.set_ylabel("Hour", labelpad=20)
ax.set_title("Plays by Hour and Day of the Week")
plt.savefig("../images/hour_and_day.png", dpi=96, bbox_inches="tight")
plt.show()
