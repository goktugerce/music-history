import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

import time_columns_adder

from html_template import *

reload(sys)
sys.setdefaultencoding("utf8")

df = pd.read_csv("../data/all_scrobbles_last.csv", encoding="utf-8")
scrobbles = df.drop("Date", axis=1)
scrobbles = time_columns_adder.add_time_columns(df, scrobbles)

day_counts = scrobbles["exact_date"].value_counts().sort_values(ascending=False)

def convert_date_to_string(x):
    string = "new Date("
    split = x.split("-")
    string += split[2] + ","
    string += str(int(split[1])-1) + ","
    string += str(int(split[0])) + ")"
    return string

html_data = ""
for index, row in day_counts.iteritems():
    string = "["
    string += convert_date_to_string(index)
    string += ","
    string += str(row)
    string += "]"
    html_data += string + ",\n"

html_data = html_data[:-2]

html = html_calendar_chart.format(html_data)

f = open("day_history_chart.html", "w")
f.write(html)
f.close()