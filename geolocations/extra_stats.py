import pandas as pd

df = pd.read_csv("../data/all_scrobbles.csv", encoding="utf-8")
occs = df["Artist"].value_counts()

places = pd.read_csv("data/info.csv", encoding="utf-8")

for index, count in occs.iteritems():
    places.loc[places["name"] == index, "PlayCount"] = count

count_by_place = {}
unique_places = places["place"].unique()
for place in unique_places:
    count_by_place[place] = places.loc[places["place"] == place, "PlayCount"].sum()

places = pd.Series(count_by_place, name="PlayCount")
places.index.name = "Place"
places = places.reset_index()
places = pd.DataFrame(places)
places.dropna(axis=0, inplace=1)
places.dropna(axis=1, inplace=1)

coordinates = pd.read_csv("data/coordinates.csv", encoding="utf-8")
for index, row in places.iterrows():
    coordinates.loc[coordinates["Place"] == row["Place"], "PlayCount"] = row["PlayCount"]

split_df = coordinates["Coordinates"].apply(lambda x: pd.Series(x.split(",")))
split_df.columns = ["Latitude", "Longitude"]
split_df = pd.concat([split_df, coordinates["PlayCount"]], axis=1)
split_df.to_csv("data/coordinates_with_playcounts.csv", index=None, encoding="utf-8")