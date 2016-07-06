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

year_counts = scrobbles["year"].value_counts().sort_index()

x = year_counts.index
y = year_counts.values

plt.plot(x, y, "-", marker="o", color="#48466D", linewidth=3)
plt.xticks(x, x)
plt.title("Songs played per year")
plt.xlabel("Year", labelpad=20)
plt.ylabel("Play Count", labelpad=20)
plt.ylim([0, max(y) * 1.2])
plt.savefig("../images/year_by_year.png", dpi=96, bbox_inches="tight")
plt.show()
