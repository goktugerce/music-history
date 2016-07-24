import pandas as pd

df = pd.read_csv("data/songs.csv", encoding = "utf-8")
print(df[df["Duration"].isnull()].head())