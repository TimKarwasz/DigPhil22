# external modules
import operator
import csv
import argparse
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# own modules
from helpers import multireplace, split_paragraphs, intersection

"""
# use this code to get the full text
import requests
URL = "https://www.gutenberg.org/cache/epub/8106/pg8106.txt"
response = requests.get(URL)
open("cook_full_text.txt", "wb").write(response.content)
"""

# The objective of this script is to parse this sentence : "latitude 18 degrees 22 minutes South, longitude 34 degrees 50 minutes west"
# to this : "18° 22’ N,34° 50’ W" so it can easily be plotted
# IMPORTANT Note: it has to be said that Cooks Logbook was very well cleaned and formatted, so this code only works if the input text is an very good shape
# also this code was created with the structure of cooks logbook in mind. To make this code work for other text some coding work would be required.
# 1. Firstly I cleanded the text by hand, removed index, preface and sketch of Cooks life and stuff at the end (license, postscript etc.)

parser = argparse.ArgumentParser(description='command line tool for parsing data')

# argument for data input filepath
parser.add_argument('-i','--inputpath', type=str,help='filepath to inputdata')

# argument for which word will be choosen as the start of parsing (check below for example)
parser.add_argument('-s','--start', type=str,help='start of parsing')

# argument for the size of the parsing lookahead
parser.add_argument('-l','--lookahead', type=int,help='size of the lookahead')

# argument for the name of the output file (only the name without the extension (.txt))
parser.add_argument('-o','--outputname', type=str,help='name of the output file')

# Example cmd usage : python parse_data.py -i cook_tim.txt -s latitude -l 14 -o out_tim

# Note:
# This script parses repetitive patterns of text, 
# the user needs to find the right inputs for the start of parsing and the lookahead based on the text they are working with.
# For our text "latitude" as start of parsing with a lookahead of 14 worked pretty well.


args = parser.parse_args()


# 1. specify the data input here 
with open(args.inputpath, encoding='utf8', mode="r") as f:
    #flat_list=[word.lower() for line in f for word in line.split()]
    contents = f.read().lower()


# 2. split the text into paragraphs
paragraphs = split_paragraphs(contents)


# 3. find the index of the start of parsing in each paragraph
indices = []
for paragraph in paragraphs:
    if args.start in paragraph.split():
        indices.append(paragraph.split().index(args.start))
    else:
        indices.append(None)


# 4. then go over all the paragraphes and find the whole sentences (with the lookahead)
geo_results = []
weather_results = []
# these were used for the first attempt of getting weather data which proved inferior to the second attempt
"""
WEATHER_ADJECTIVES = ["brezzy", "cloudy", "cloud", "wind", "windy", "brezzes", "gales", "rain", "rainy", 
                      "sunshine", "snow", "snowy","hazey", "squall", "squalls", "hot", "cold", "arid", "foggy",
                      "sunny", "scorcher", "blistering", "tropical", "brisk", "biting", "bleak", "icy", "harsh",
                      "crisp", "cloudless", "still", "windless", "gale-force", "sultry", "gusty", "humid", "muggy"
                      "murky", "torrential", "blizzard", "fog", "fogbound", "grey", "hurricane", "mist", "misty",
                      "thunder", "thunderstorm", "thundercloud", "tsnunami", "typhoon"]
"""

for index,paragraph in zip(indices,paragraphs):
    if index: 
        splitted_paragraph = paragraph.split()
        gps_text = splitted_paragraph[index-1:index + args.lookahead + 3]
        # check if lattiude and longtiude occur to get only valid gps data
        if "latitude" in gps_text and "longitude" in gps_text:
            lat_list = []
            long_list = []
            lat_result = []
            long_result = []
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

            geo_results.append((" ".join(lat_result), " ".join(long_result)))


            # 5. get weather data here

            """
            # Attempt 1: Matching weather adjectives and saving the context data (bad)
            if intersection(WEATHER_ADJECTIVES, splitted_paragraph):
                # if there are matches get context
                contexts = []
                for match in intersection(WEATHER_ADJECTIVES, splitted_paragraph):
                    # this line looks complex but only slices the paragraph to get the context words around the match
                    contexts.append(splitted_paragraph[splitted_paragraph.index(match)-3:splitted_paragraph.index(match)+3])
                weather_results.append(contexts)
            else:
                weather_results.append(None)
            """

            # Attempt 2: Getting the first sentences of each paragraph (good)
            weather_results.append(" ".join(tokenizer.tokenize(paragraph.strip())[0:2]))

    else:
        pass
        


# 6. parse the sentences as they look this right now: ('18 degrees 22 minutes south,', '34 degrees 50 minutes west.')
# replace degree with °, minute with ’, seconds with ″, and the long names (north, south, ...) with N,S,E,W
# note: I had to manually clean some entries later as they caused problems with the plotting of the data
lat_formatted_results = []
long_formatted_results = []

replacement_dict_lat = {" minutes": "’", " seconds": "’’", " degrees": "°", "south": "S", "south;": "S",
                         "south,": "S", " degree": "°", "south": "S", "minute": "’", "north": "N", "north;": "N",
                         "north," : "N", ";": "", ",": "",".":""}
replacement_dict_long = {" minutes": "’", " seconds": "’’", " degrees": "°", "east": "E", "east;": "E",
                         "east,": "E", " degree": "°", "east": "E", "minute": "’", "west": "W", "west;": "W",
                         "west," : "W", ";": "", ",": "",".":""}

for lat,longi in geo_results:
    if lat and longi:
        lat_formatted_results.append(multireplace(lat, replacement_dict_lat))
        long_formatted_results.append(multireplace(longi, replacement_dict_long))



# 7. some longitude values are over 180 degrees, this bit of code accounts for that
new_long_results = []
for lat,longi in zip(lat_formatted_results,long_formatted_results):
    lst = longi.split()
    degrees = lst[0]
    if degrees != "W" and degrees != "E":
        lst.pop(0)
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

    long_formatted_results = new_long_results


# 8. write the parsed data
# some rows were incomplete, so I had to manually complete them
# e.g "30° 46’ N,16° 8’" here the W in the end is missing, but based on the entries before and after corrput ones
# this can easily be fixed
with open(args.outputname + ".csv", mode='w', newline='') as csv_file:
    fieldnames = ['lat', 'long', 'weather']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for lat,longi,weather in zip(lat_formatted_results,long_formatted_results, weather_results):
        writer.writerow({'lat': lat, 'long': longi, 'weather': weather})


