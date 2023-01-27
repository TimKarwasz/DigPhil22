import operator
import csv
from helpers import multireplace

"""
# use this code to get the full text
import requests
URL = "https://www.gutenberg.org/cache/epub/8106/pg8106.txt"
response = requests.get(URL)
open("cook_full_text.txt", "wb").write(response.content)
"""
# The objective of this script is to parse this sentence : "latitude 18 degrees 22 minutes South, longitude 34 degrees 50 minutes west"
# to this : "18° 22’ N,34° 50’ W" so it can easily be plotted
# 1. Firstly I cleanded the text by hand, removed index, preface and sketch of Cooks life and stuff at the end (license, postscript etc.)

wordCount = 0
wordList = []
# specify the data input here 
with open('cook_tim.txt', encoding='utf8', mode="r") as f:
    #contents = f.read() 
    flat_list=[word.lower() for line in f for word in line.split()]


# 2. find all indices for latitude
indices = [i for i, x in enumerate(flat_list) if x == "latitude"]

gps_texts = []
gps_coordinates = []

# 3. then go over all the indices and find the whole sentences
results = []
for index in indices:
    gps_text = list(operator.itemgetter(*list(range(index,index + 14)))(flat_list))
    # check if lattiude and longtiude occur
    if "latitude" in gps_text and "longitude" in gps_text:
        lat_list = []
        long_list = []
        lat_result = []
        long_result = []
        gps_texts.append(gps_text)
        # find start of longitude text
        longitude_index = gps_text.index("longitude")
        # put words in the right lists for easier parsing
        # e.g. in the sentence "latitude 18 degrees 22 minutes South, longitude 34 degrees 50 minutes west"
        #  "latitude 18 degrees 22 minutes South" comes in the latitude list and the rest in the longitude list
        for idx, x in enumerate(gps_text):
            if idx < longitude_index:
                lat_list.append(x)
            else:
                long_list.append(x)
        #filter numbers and direction (north or south for latitude and east or west for longitude)
        for word in lat_list:
            #if word.isdigit() or word in ["north,","north,","north.","north;","north?","north!","north:",
            #"south,","south.","south;","south?","south!","south:","south", ] :
            #    lat_result.append(word)
            # only take words that we need for parsing,
            # because we check if for example "north" is in the word we are currently looking at we also take other froms of north e.g. "north!" or "north,"
            if word.isdigit() or "south" in word or "north" in word or "minute" in word or "second" in word or "degree" in word:
                lat_result.append(word)

        for word in long_list:
            #if word.isdigit() or word in ["west,","west,","west.","west;","west?","west!","west:",
            #"east,","east","east;","east?","east!","east:","east", ] :
            #    long_result.append(word)
            # same as above for clause
            if word.isdigit() or "east" in word or "west" in word or "minute" in word or "second" in word or "degree" in word:
                long_result.append(word)
        # print outs for manual debugging
        #print(f"lat result:{lat_result}")
        #print(f"long result:{long_result}")
        #print(f"Original :{gps_text}")
        #print("#"*20)


        results.append((" ".join(lat_result), " ".join(long_result)))

# 4. parse the sentences as they look this atm : ('18 degrees 22 minutes south,', '34 degrees 50 minutes west.')
# replace degree with °, minute with ’, seconds with ″, and the long names (north, south, ...) with N,S,E,W
# note: I had to remove the seconds entries later manually as they caused problems with the plotting of the data
lat_formatted_results = []
long_formatted_results = []

replacement_dict_lat = {" minutes": "’", " seconds": "’’", " degrees": "°", "south": "S", "south;": "S",
                         "south,": "S", " degree": "°", "south": "S", "minute": "’", "north": "N", "north;": "N",
                         "north," : "N", ";": "", ",": "",".":""}
replacement_dict_long = {" minutes": "’", " seconds": "’’", " degrees": "°", "east": "E", "east;": "E",
                         "east,": "E", " degree": "°", "east": "E", "minute": "’", "west": "W", "west;": "W",
                         "west," : "W", ";": "", ",": "",".":""}

for lat,longi in results:
    if lat and longi:
        lat_formatted_results.append(multireplace(lat, replacement_dict_lat))
        long_formatted_results.append(multireplace(longi, replacement_dict_long))

"""
# this is only relevant for the last 6 chapters as some degree values go over 180 there
new_long_results = []
for lat,longi in zip(lat_formatted_results,long_formatted_results):
    lst = longi.split()
    degrees = lst[0]
    lst.pop(0)
    # make up for the fact that some longitude values are above 180 degrees
    degrees = degrees.replace("°", "")
    if int(degrees) > 180:
        difference = int(degrees) - 180
        real_long = 180 - difference
        # more debugging
        #print(f"org long : {degrees}, new long: {real_long}")
        #print(new_degrees)
        #print(lst)
        # the following few lines construct the "34° 50’ W" sentence again
        new_degrees = str(real_long) + '°'
        new_list= [new_degrees] + lst
        new_list = " ".join(new_list)
        new_list = new_list.replace("W", "E")
        longi = new_list
    new_long_results.append(longi)
"""


# 5. write the parsed data
# some rows were incomplete, so I had to manually complete them
# e.g "30° 46’ N,16° 8’" here the W in the end is missing, but based on the entries before and after corrput ones
# this can easily be fixed
with open('coordinates_test.csv', mode='w', newline='') as csv_file:
    fieldnames = ['lat', 'long']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for lat,longi in zip(lat_formatted_results,long_formatted_results):
        writer.writerow({'lat': lat, 'long': longi})
