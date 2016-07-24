import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../spotify/data/songs.csv", encoding="utf-8")

total_ms = df["Duration"].sum()
total_sec = total_ms / 1000
total_min = total_sec / 60
total_hour = total_min / 60
m, s = divmod(total_sec, 60)
h, m = divmod(m, 60)
print "%d:%02d:%02d" % (h, m, s)
print(total_sec)
print(total_min)
# print(df["Track"].value_counts())