# plot geo data
import pandas as pd
import csv
from dataprep.clean import clean_lat_long
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


pd.options.display.max_rows = None

# load data from the csv file
lats = []
longs = []
with open('coordinates_clean_copy.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')

    # read data
    for row in reader:
        lats.append(row[0].replace("’", "′"))
        longs.append(row[1].replace("’", "′"))

# check that data is not null
coords = []
for lat,longi in zip(lats,longs):
    if lat != "lat":
        # reconstruct coordinates
        coords.append(lat + ", "  + longi)

df = pd.DataFrame(coords,columns =['coord'])

# convert DMS (Degree Minutes Seconds) GPS data to decimal
# make sure that every coordinate is converted (I had to manually clean a bit and help with the conversin )
df2 = clean_lat_long(df, 'coord', split=True)

# introduce colors for each point to make it more clearly in the plot
colors = ["red"] * 289 + ["blue"] * 194
df['colors'] = colors

# draw plot
fig = go.Figure(go.Scattergeo(
    lat=df2['latitude'],
    lon=df2['longitude'],
    marker = {'color' : df['colors']}
    ))
fig.show()

