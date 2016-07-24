import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import time_functions


def add_time_columns(df, scrobbles):
    scrobbles["timestamp"] = pd.to_datetime(df["Date"])
    scrobbles["year"] = scrobbles["timestamp"].apply(time_functions.get_year)
    scrobbles["month"] = scrobbles["timestamp"].apply(time_functions.get_month)
    scrobbles["day"] = scrobbles["timestamp"].apply(time_functions.get_day)
    scrobbles["hour"] = scrobbles["timestamp"].apply(time_functions.get_hour)
    scrobbles["minute"] = scrobbles["timestamp"].apply(time_functions.get_min)
    scrobbles["second"] = scrobbles["timestamp"].apply(time_functions.get_sec)
    scrobbles["weekday"] = scrobbles["timestamp"].apply(time_functions.get_day_of_the_week)
    scrobbles["timestamp"] = scrobbles["timestamp"].apply(time_functions.convert_timezone)
    scrobbles["exact_date"] = scrobbles["timestamp"].apply(time_functions.get_exact_date)
    # scrobbles.drop("timestamp", axis=1, inplace=1)
    scrobbles = scrobbles[scrobbles['year'] > 1970]

    return scrobbles