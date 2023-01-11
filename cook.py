import requests
import operator
import csv


"""
# use this code to get the full text
URL = "https://www.gutenberg.org/cache/epub/8106/pg8106.txt"
response = requests.get(URL)
open("cook_full.txt", "wb").write(response.content)
"""

# 1 . Firstly I cleanded the text by hand, removed index, preface and sketch of Cooks life and stuff at the end (license, postscript etc.)

wordCount = 0
wordList = []
with open('cook_lea.txt', encoding='utf8', mode="r") as f:
    #contents = f.read() 
    flat_list=[word.lower() for line in f for word in line.split()]


# find all indices for latitude
indices = [i for i, x in enumerate(flat_list) if x == "latitude"]

gps_texts = []
gps_coordinates = []

results = []
for index in indices:
    gps_text = list(operator.itemgetter(*list(range(index,index+14)))(flat_list))
    # check if lattiude and longtiude occur
    if "latitude" in gps_text and "longitude" in gps_text:
        lat_list = []
        long_list = []
        lat_result = []
        long_result = []
        gps_texts.append(gps_text)
        #find start of longitude text
        longitude_index = gps_text.index("longitude")
        for idx, x in enumerate(gps_text):
            if idx < longitude_index:
                lat_list.append(x)
            else:
                long_list.append(x)
        #filter numbers and direction (north or south for lat and east or west for long)
        for word in lat_list:
            #if word.isdigit() or word in ["north,","north,","north.","north;","north?","north!","north:",
            #"south,","south.","south;","south?","south!","south:","south", ] :
            #    lat_result.append(word)
            if word.isdigit() or "south" in word or "north" in word or "minute" in word or "second" in word or "degree" in word:
                lat_result.append(word)

        for word in long_list:
            #if word.isdigit() or word in ["west,","west,","west.","west;","west?","west!","west:",
            #"east,","east","east;","east?","east!","east:","east", ] :
            #    long_result.append(word)
            if word.isdigit() or "east" in word or "west" in word or "minute" in word or "second" in word or "degree" in word:
                long_result.append(word)
        #print(f"lat result:{lat_result}")
        #print(f"long result:{long_result}")
        #print(f"Original :{gps_text}")
        #print("#"*20)


        results.append((" ".join(lat_result), " ".join(long_result)))

# replace degree with °, minute with ’, seconds with ″, and the long names with N,S,E,W
lat_formatted_results = []
long_formatted_results = []
for lat,longi in results:
    if lat and longi:
        lat = lat.replace(" minutes","’").replace(" seconds", "’’").replace(" degrees", "°").replace("south,", "S").replace("south;", "S").replace(" degree", "°").replace("south", "S").replace("minute", "’").replace("north", "N").replace("north;", "N").replace("north,", "N").replace(";", "").replace(",","").replace(".","")
        longi= longi.replace(" minutes","’").replace(" seconds", "’’").replace(" degrees", "°").replace("east,", "E").replace("east;", "E").replace(" degree", "°").replace("east", "E").replace("minute", "’").replace("west", "W").replace("west;", "W").replace("west,", "W").replace(";", "").replace(",","").replace(".","")
        
        lat_formatted_results.append(lat)
        long_formatted_results.append(longi)


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
        #print(f"org long : {degrees}, new long: {real_long}")
        new_degrees = str(real_long) + '°'
        #print(new_degrees)
        #print(lst)
        new_list= [new_degrees] + lst
        new_list = " ".join(new_list)
        new_list = new_list.replace("W", "E")

        longi = new_list

    new_long_results.append(longi)

with open('coordinates_lea_new.csv', mode='w', newline='') as csv_file:
    fieldnames = ['lat', 'long']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for lat,longi in zip(lat_formatted_results,new_long_results):
        writer.writerow({'lat': lat, 'long': longi})