import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding("utf8")

month = "2016-05"

df = pd.read_csv("data/all_scrobbles_last.csv", encoding="utf-8")
df = df[df["Date"].str.startswith(month)]
df.to_csv("data/" + month + ".csv", index=None, encoding="utf-8")
