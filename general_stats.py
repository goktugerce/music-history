import pandas as pd
import sys
import pytz
reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("data/all_scrobbles_last.csv", encoding="utf-8")
df["timestamp"] = pd.to_datetime(df.Date)
ts_utc = df["timestamp"].dt.tz_localize("UTC")
df["timestamp"] = ts_utc.dt.tz_convert("Europe/Istanbul")

df["Year"] = df["timestamp"].dt.year
print(df.groupby(["Year"]).Artist)