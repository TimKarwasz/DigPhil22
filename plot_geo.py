# plot geo data
import pandas as pd
import csv
from dataprep.clean import clean_lat_long
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly
import plotly.graph_objects as go
import plotly.express as px
import chart_studio
import chart_studio.plotly as py


"""
Note: 
This script was mainly used for converting the degree minutes seconds (DMS) coordinates values
to decimal values and to create a nice csv for use with:
https://chart-studio.plotly.com where I created the plot

"""

pd.options.display.max_rows = None

# load data from the csv file
lats = []
longs = []
weather = []

with open('new_combined.csv', 'r', encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=';')

    # read data
    for row in reader:
        #print(row)
        lats.append(row[0].replace("’", "′"))
        longs.append(row[1].replace("’", "′"))
        weather.append(row[2])

# check that data is not null
coords = []
for lat,longi in zip(lats,longs):
    if lat != "lat":
        # reconstruct coordinates
        coords.append(lat + ", "  + longi)

df = pd.DataFrame(coords,columns =['coord'])
df["weather"] = weather

# convert DMS (Degree Minutes Seconds) GPS data to decimal
# make sure that every coordinate is converted (I had to manually clean a bit and help with the conversin )
df2 = clean_lat_long(df, 'coord', split=True)
#print(df2)

# introduce colors for each point to make it more clearly in the plot (must be put manually as they depend on the data)
colors = ["red"] * 216 + ["blue"] * 180
df['colors'] = colors

# draw plot
fig = go.Figure(go.Scattergeo(
    lat=df2['latitude'],
    lon=df2['longitude'],
    marker = {'color' : df['colors']}
    ))

fig.show()

with open("out" + ".csv", mode='w', newline='') as csv_file:
    fieldnames = ['latitude', 'longitude', "color", "weather"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=",")
    writer.writeheader()
    for lat,longi,color,weather in zip(df2['latitude'],df2['longitude'],df["colors"], df["weather"]):
        writer.writerow({'latitude': lat, 'longitude': longi, "color": color, "weather": weather})

# manual html code for the plot (very ugly)
fig.write_html(file='C:\\Users\\Tim\\Desktop\\TimProject\\DH\\DigPhil22\\b.html')
